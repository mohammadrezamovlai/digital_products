from django.contrib import admin
from .models import AppUser

@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    list_display = (
        'username','id', 'full_name', 'phone', 'email', 'role',
        'is_active', 'is_verified', 'last_seen', 'created_at'
    )
    list_filter = ('username','role', 'is_active', 'is_verified', 'gender')
    search_fields = ('username','full_name', 'phone', 'email')
    readonly_fields = ('public_id', 'created_at', 'updated_at', 'last_seen')
