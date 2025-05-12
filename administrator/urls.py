from django.urls import path
from . import views

app_name = 'administrator'

urlpatterns = [
    path('', views.admin_home, name='admin_home'),
    path('matched/', views.manage_matched_items, name='manage_matched_items'),
    path('api/lost-items-by-category', views.lost_items_by_category, name='lost_items_by_category'),
]