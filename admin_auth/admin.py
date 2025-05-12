from django.contrib import admin
from .models import Admin

# Register your models here.
@admin.register(Admin)
class FoundItemAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'contact_number', 'last_login', 'date_joined',)
    list_filter = ('is_active',)
    search_fields = ('username', 'email', 'contact_number',)
    ordering = ('-date_joined',)
