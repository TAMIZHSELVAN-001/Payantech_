from django.contrib import admin
from .models import ContactMessage, UserProfile

# Register ContactMessage model
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'submitted_at')
    list_filter = ('submitted_at',)
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('submitted_at',)


# Register UserProfile model
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'user__email', 'phone')
    readonly_fields = ('created_at', 'updated_at')

