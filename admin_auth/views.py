from django.shortcuts import render, redirect
from django.urls import reverse
from .services import authenticate
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def login_page(request):
    return render(request, 'admin_auth/login.html')

@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Here you would typically check the username and password against your database
        # For demonstration, we'll just check if they are not empty
        print(authenticate(username, password))
        if username and password and authenticate(username, password):
            admin_home_url = reverse('administrator:admin_home')
            return redirect(f"{admin_home_url}?username={username}")
        else:
            return render(request, 'admin_auth/login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'admin_auth/login.html')