from django.db import models
from django.utils import timezone

class Volunteer(models.Model):
    VOLUNTEER_TYPES = [
        ('event', 'Event Day Volunteer'),
        ('packing', 'Pre-event Packing'),
        ('both', 'Both'),
    ]
    
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    volunteer_type = models.CharField(max_length=20, choices=VOLUNTEER_TYPES)
    available_date = models.DateField(null=True, blank=True)
    skills = models.TextField(blank=True, help_text="Any special skills or experience?")
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.full_name} - {self.volunteer_type}"
    
    class Meta:
        ordering = ['-created_at']

class Donor(models.Model):
    DONATION_TYPES = [
        ('money', 'Monetary Donation'),
        ('items', 'Item Donation'),
        ('sponsorship', 'Child Sponsorship'),
    ]
    
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    donation_type = models.CharField(max_length=20, choices=DONATION_TYPES)
    donation_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    donation_items = models.TextField(blank=True, help_text="If donating items, please list them")
    message = models.TextField(blank=True)
    is_contacted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.full_name} - {self.donation_type}"
    
    class Meta:
        ordering = ['-created_at']

class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_replied = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.subject}"
    
    class Meta:
        ordering = ['-created_at']