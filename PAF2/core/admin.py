from django.contrib import admin
from .models import Volunteer, DonationItem, Partnership, ContactMessage

@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'volunteer_type', 'status', 'created_at', 'is_contacted']
    list_filter = ['volunteer_type', 'status', 'is_contacted', 'created_at']
    search_fields = ['full_name', 'email', 'phone']
    list_editable = ['status', 'is_contacted']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Personal Information', {
            'fields': ('full_name', 'email', 'phone')
        }),
        ('Volunteer Details', {
            'fields': ('volunteer_type', 'message', 'status', 'is_contacted', 'notes')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(DonationItem)  # Changed from DonationItem
class DonationItemAdmin(admin.ModelAdmin):
    list_display = ['donor_name', 'item_category', 'quantity', 'status', 'created_at']
    list_filter = ['item_category', 'status', 'created_at']
    search_fields = ['donor_name', 'donor_email', 'item_description']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Donor Information', {
            'fields': ('donor_name', 'donor_email', 'donor_phone')
        }),
        ('Donation Details', {
            'fields': ('item_category', 'item_description', 'quantity', 'drop_off_date', 'status', 'notes')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Partnership)  # Changed from Partnership
class PartnershipAdmin(admin.ModelAdmin):
    list_display = ['contact_person', 'partner_type', 'organization_name', 'status', 'created_at']
    list_filter = ['partner_type', 'status', 'created_at']
    search_fields = ['contact_person', 'organization_name', 'email', 'proposal']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Contact Information', {
            'fields': ('contact_person', 'email', 'phone')
        }),
        ('Organization Details', {
            'fields': ('organization_name', 'partner_type')
        }),
        ('Partnership Details', {
            'fields': ('proposal', 'status', 'notes')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'inquiry_type', 'created_at', 'is_replied']
    list_filter = ['inquiry_type', 'is_replied', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    list_editable = ['is_replied']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Sender Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Message Details', {
            'fields': ('inquiry_type', 'subject', 'message', 'is_replied', 'reply', 'replied_by', 'replied_at')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )