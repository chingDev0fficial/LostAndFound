from django.views.decorators.csrf import csrf_exempt
from .models import LostItem
import json

@csrf_exempt
def process_lost_item(request):
    """
    Function to handle the lost item report.
    """
    # Logic for reporting a lost item
    # Handle file uploads
    item_image = request.FILES.get('item-image')
    
    # Create new lost item record
    lost_item = LostItem(
        item_name=request.POST.get('item_name'),
        category=request.POST.get('category'),
        date_lost=request.POST.get('date_lost'),
        time_lost=request.POST.get('time_lost'),
        location=request.POST.get('location'),
        description=request.POST.get('description'),
        image=item_image if item_image else None,
        
        # Contact info
        full_name=request.POST.get('full_name'),
        email=request.POST.get('email'),
        phone=request.POST.get('phone'),
        preferred_contact=request.POST.get('contact-method') 
    )
    lost_item.save()
    # print([request.POST.get('item-name'), request.POST.get('category'), request.POST.get('date-lost'), request.POST.get('time-lost'), request.POST.get('location-lost'), request.POST.get('description'), request.POST.get('fullname'), request.POST.get('email'), request.POST.get('phone'), request.POST.get('contact-method')])
    # return [request.POST.get('item_name'), request.POST.get('category'), request.POST.get('date_lost'), request.POST.get('time_lost'), request.POST.get('location'), request.POST.get('description'), request.POST.get('full_name'), request.POST.get('email'), request.POST.get('phone'), request.POST.get('contact-method')]