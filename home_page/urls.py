from django.urls import path
from . import views

app_name = 'home_page'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('submit-lost-item/', views.item_lost_report),
    path('recognize-image/', views.recognize_image),
    path('submit-found-item/', views.item_found_report)
]