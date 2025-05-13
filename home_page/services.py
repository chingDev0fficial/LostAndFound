from django.conf import settings
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import LostItem, FoundItem, MatchedItem
from .ml_services import ItemMatcher
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from sentence_transformers import SentenceTransformer

def notify_admin_dashboard():
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'reports',  # Group name
        {
            'type': 'send_report_update',
            'message': 'Updated counts',
            'total_found': FoundItem.objects.count(),
            'total_lost': LostItem.objects.count(),
            'total_matched': MatchedItem.objects.count(),
        }
    )

@csrf_exempt
def process_lost_item(request):

    # Logic for reporting a lost item
    # Handle file uploads
    try:
        item_image = request.FILES.get('item-image')
        time = request.POST.get('time-lost')

        print(request.POST.get('location-lost'))
        
        # Create new lost item record
        lost_item = LostItem(
            item_name=request.POST.get('item-name'),
            category=request.POST.get('category'),
            date_lost=request.POST.get('date-lost'),
            time_lost=time if time else None,
            location=request.POST.get('location-lost'),
            description=request.POST.get('description'),
            image=item_image if item_image else None,
            
            # Contact info
            full_name=request.POST.get('fullname'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone')
        )
        lost_item.save()

        notify_admin_dashboard()

        # Check for matches in lost items
        matcher = ItemMatcher()
        potential_matches = matcher.match_items(
            lost_item,
            FoundItem.objects.filter(status='pending'),
            threshold=0.7
        )

        if potential_matches:
            print(f'Processing potential matches: {potential_matches}')
            match = potential_matches[0]
            found_item = match['found_matched']

            # Update statuses
            lost_item.status = 'matched'
            found_item.status = 'matched'
            lost_item.save()
            found_item.save()

            # Store the match in MatchedItem
            matched_item = MatchedItem(
                lost_item=lost_item,
                found_item=found_item,
                matched_by="System",
                confidence_score=match['similarity'] * 100
            )
            matched_item.save()
            notify_admin_dashboard()

            print(f'Matched Item: {matched_item}')

            # Send notifications
            send_match_notification(
                lost_item,
                found_item,
                match['similarity'] * 100
            )

        return {
            'success': True,
            'message': 'Found item reported successfully',
            'matches_found': len(potential_matches)
        }
    except Exception as e:
        return {
            'success': False,
            'message': str(e)
        }

def process_found_item(request):

    # Logic for reporting a found item
    # Handle file uploads
    try:
        item_image = request.FILES.get('item-image')
        
        # Create new found item record
        found_item = FoundItem(
            image=item_image,
            category=request.POST.get('predicted-category'),
            item_name=request.POST.get('item-name'),
            location=request.POST.get('location-found'),
            date_found=request.POST.get('date-found'),
            time_found=request.POST.get('time-found'),
            description=request.POST.get('description'),
            
            # Finder info
            finder_name=request.POST.get('finder-name'),
            finder_email=request.POST.get('finder-email'),
            finder_phone=request.POST.get('finder-phone')
        )
        found_item.save()

        notify_admin_dashboard()

        # Check for matches in lost items
        matcher = ItemMatcher()
        potential_matches = matcher.match_items(
            found_item,
            LostItem.objects.filter(status='pending')
        )

        print(f'Potential Matches: {True if potential_matches else False}')

        if potential_matches:
            print(f'Processing potential matches: {potential_matches}')
            match = potential_matches[0]
            lost_item = match['found_matched']

            # Update statuses
            found_item.status = 'matched'
            lost_item.status = 'matched'
            found_item.save()
            lost_item.save()

            print(f'Found Item: {found_item}')
            print(f'Lost Item: {lost_item}')

            # Store the match in MatchedItem
            matched_item = MatchedItem(
                lost_item=lost_item,
                found_item=found_item,
                matched_by="System",
                confidence_score=match['similarity'] * 100
            )
            matched_item.save()

            notify_admin_dashboard()

            print(f'Matched Item: {matched_item}')

            # Send notifications
            send_match_notification(
                found_item,
                lost_item,
                match['similarity'] * 100
            )

        return {
            'success': True,
            'message': 'Found item reported successfully',
            'matches_found': len(potential_matches)
        }
    except Exception as e:
        return {
            'success': False,
            'message': str(e)
        }
    
def send_match_notification(item, matched_item, similarity_score):
    """Send notifications with complete contact information"""
    
    # Determine if this is a lost or found item notification
    if isinstance(item, LostItem):
        owner = {
            'name': item.full_name,
            'email': item.email,
            'phone': item.phone
        }
        # finder = {
        #     'name': matched_item.finder_name,
        #     'email': matched_item.finder_email,
        #     'phone': matched_item.finder_phone
        # }
        # item_details = {
        #     'name': item.item_name,
        #     'category': item.category,
        #     'location': matched_item.location,
        #     'date': matched_item.date_found
        # }
    else:
        owner = {
            'name': matched_item.full_name,
            'email': matched_item.email,
            'phone': matched_item.phone
        }
        # finder = {
        #     'name': item.finder_name,
        #     'email': item.finder_email,
        #     'phone': item.finder_phone
        # }
        # item_details = {
        #     'name': matched_item.item_name,
        #     'category': matched_item.category,
        #     'location': item.location,
        #     'date': item.date_found
        # }

    # Send email notification
    # message_founder = f"""
    # Good news! We found a potential match for your found item.
    
    # Match Details:
    # - Similarity Score: {similarity_score:.1f}%
    # - Item: {item_details['name']}
    # - Category: {item_details['category']}
    # - Location Found: {item_details['location']}
    # - Date Found: {item_details['date']}

    # Loser's Contact Information:
    # - Name: {owner['name']}
    # - Email: {owner['email']}
    # - Phone: {owner['phone']}
    
    # Wait for the loser's to contact you via email or phone.
    # """

    message_loser = f"""
    Good news! Your lost item has been found.

    The person who found your item is on their way to submit it to the USC.
    Please wait until the USC officially receives the item and issues a transaction code for your claim.
    """

    # send_mail(
    #     subject='Match Found for Your found Item',
    #     message=message_founder,
    #     from_email=settings.DEFAULT_FROM_EMAIL,
    #     recipient_list=[finder['email']],
    #     fail_silently=False
    # )

    send_mail(
        subject='Match Found for Your Lost Item',
        message=message_loser,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[owner['email']],
        fail_silently=False
    )