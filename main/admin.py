from django.contrib import admin
from .models import ContactMessage, Event

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'subject', 'created_at', 'is_replied']
    list_filter = ['subject', 'is_replied', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'message']
    list_editable = ['is_replied']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Sender Information', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Message Details', {
            'fields': ('subject', 'message', 'is_replied', 'reply', 'replied_by', 'replied_at')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'venue', 'date', 'time_start', 'time_end', 'is_upcoming']
    list_filter = ['is_upcoming', 'date']
    search_fields = ['title', 'venue', 'description']
    list_editable = ['is_upcoming']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Event Details', {
            'fields': ('title', 'venue', 'date', 'time_start', 'time_end', 'description', 'image', 'is_upcoming')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )