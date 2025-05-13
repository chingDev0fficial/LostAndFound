from django.contrib import admin
from .models import LostItem, FoundItem, MatchedItem
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

@admin.register(MatchedItem)
class MatchedItemAdmin(admin.ModelAdmin):
    list_display = ('lost_item', 'found_item', 'matched_at', 'matched_by', 'confidence_score')
    search_fields = ('lost_item__item_name', 'found_item__item_name', 'matched_by')
    list_filter = ('matched_at', 'matched_by')