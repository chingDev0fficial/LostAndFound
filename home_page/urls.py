from django.urls import path
from . import views

app_name = 'home_page'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('submit-lost-item/', views.item_lost_report),
]