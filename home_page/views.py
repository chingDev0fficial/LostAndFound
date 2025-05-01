from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .services import process_lost_item

# Create your views here.
def home(request):
    return render(request, 'home_page/home.html')

def about(request):
    return render(request, 'home_page/about.html')

def contact(request):
    return render(request, 'home_page/contact.html')

@csrf_exempt
def item_lost_report(request):
    if request.method == 'POST':
        try:
            process_lost_item(request)
            return JsonResponse({
                'success': True,
                'message': 'Successfully Submitted the Form'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
        
    return JsonResponse({'success': False, 'message': 'Invalid request method'})