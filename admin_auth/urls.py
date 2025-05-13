from django.urls import path
from . import views

app_name = 'admin_auth'

urlpatterns = [
    path('', views.login_page),
    path('login/', views.login, name='login'),
]