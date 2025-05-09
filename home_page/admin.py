from django.contrib import admin
from .models import LostItem, FoundItem
# Register your models here.
@admin.register(FoundItem)
class FoundItemAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'category', 'location', 'date_found', 'finder_name')
    list_filter = ('category', 'date_found')
    search_fields = ('item_name', 'description', 'finder_name')
    date_hierarchy = 'date_found'

@admin.register(LostItem)
class LostItemAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'category', 'location', 'date_lost', 'full_name')
    list_filter = ('category', 'date_lost')
    search_fields = ('item_name', 'description', 'full_name')
    date_hierarchy = 'date_lost'