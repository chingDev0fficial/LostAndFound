from django.shortcuts import render
from admin_auth.models import Admin
from django.http import JsonResponse
from home_page.models import LostItem
from django.db.models import Count

# Create your views here.
def admin_home(request):
    user_admin = Admin.objects.filter(username=request.GET.get('username')).first()
    request.session['user_id'] = user_admin.id
    request.session['name'] = f"{user_admin.first_name} {user_admin.last_name}"
    request.session['username'] = user_admin.username
    request.session['email'] = user_admin.email
    request.session['contact_number'] = user_admin.contact_number  
    request.session['last_login'] = user_admin.last_login.strftime('%Y-%m-%d %H:%M:%S') if user_admin.last_login else None
    request.session['date_joined'] = user_admin.date_joined.strftime('%Y-%m-%d %H:%M:%S')
    return render(request, 'administrator/admin.html')

def manage_matched_items(request):
    return render(request, 'administrator/manage_item.html')

def lost_items_by_category(request):
    data = (
        LostItem.objects.values('category')
        .annotate(count=Count('category'))
        .order_by('category')
    )
    return JsonResponse(list(data), safe=False)