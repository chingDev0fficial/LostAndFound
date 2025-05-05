from .models import LostItem, FoundItem
from .ml_services import send_match_notification, ItemMatcher, load_model
from django.views.decorators.csrf import csrf_exempt
from sentence_transformers import SentenceTransformer

@csrf_exempt
def process_lost_item(request):
    """
    Function to handle the lost item report.
    """

    # Logic for reporting a lost item
    # Handle file uploads
    try:
        item_image = request.FILES.get('item-image')

        print(request.POST.get('location-lost'))
        
        # Create new lost item record
        lost_item = LostItem(
            item_name=request.POST.get('item-name'),
            category=request.POST.get('category'),
            date_lost=request.POST.get('date-lost'),
            time_lost=request.POST.get('time-lost'),
            location=request.POST.get('location-lost'),
            description=request.POST.get('description'),
            image=item_image if item_image else None,
            
            # Contact info
            full_name=request.POST.get('fullname'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone')
        )
        lost_item.save()

        # Check for matches in lost items
        matcher = ItemMatcher()
        potential_matches = matcher.match_items(
            lost_item,
            LostItem.objects.filter(status='pending'),
            threshold=0.7
        )

        # Send notifications for matches
        for match in potential_matches:
            send_match_notification(
                lost_item,
                match['lost_item'],
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
    # print([request.POST.get('item-name'), request.POST.get('category'), request.POST.get('date-lost'), request.POST.get('time-lost'), request.POST.get('location-lost'), request.POST.get('description'), request.POST.get('fullname'), request.POST.get('email'), request.POST.get('phone'), request.POST.get('contact-method')])
    # return [request.POST.get('item_name'), request.POST.get('category'), request.POST.get('date_lost'), request.POST.get('time_lost'), request.POST.get('location'), request.POST.get('description'), request.POST.get('full_name'), request.POST.get('email'), request.POST.get('phone'), request.POST.get('contact-method')]

def process_found_item(request):
    """
    Function to handle the found item report.
    """

    # Logic for reporting a found item
    # Handle file uploads
    try:
        item_image = request.FILES.get('item-image')
        
        # Create new found item record
        found_item = FoundItem(
            item_image=item_image,
            predicted_category=request.POST.get('predicted-category'),
            item_name=request.POST.get('item-name'),
            location_found=request.POST.get('location-found'),
            date_found=request.POST.get('date-found'),
            time_found=request.POST.get('time-found'),
            description=request.POST.get('description'),
            
            # Finder info
            finder_name=request.POST.get('finder-name'),
            finder_email=request.POST.get('finder-email'),
            finder_phone=request.POST.get('finder-phone')
        )
        found_item.save()

        # Check for matches in lost items
        matcher = ItemMatcher()
        potential_matches = matcher.match_items(
            found_item,
            LostItem.objects.filter(status='pending'),
            threshold=0.7
        )

        # Send notifications for matches
        for match in potential_matches:
            send_match_notification(
                found_item,
                match['lost_item'],
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