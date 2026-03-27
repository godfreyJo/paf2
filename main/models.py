from django.db import models
from django.utils import timezone

class ContactMessage(models.Model):
    """Model to store contact form messages"""
    
    INQUIRY_TYPES = [
        ('general', 'General Inquiry'),
        ('donation', 'Donation'),
        ('volunteer', 'Volunteer'),
        ('partnership', 'Partnership'),
        ('media', 'Media/Press'),
        ('other', 'Other'),
    ]
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200, choices=INQUIRY_TYPES, default='general')
    message = models.TextField()
    reply = models.TextField(blank=True, help_text="Staff reply to this message")
    replied_by = models.CharField(max_length=100, blank=True)
    replied_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_replied = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.subject}"
    
    def mark_as_replied(self, staff_name):
        """Mark message as replied"""
        self.is_replied = True
        self.replied_by = staff_name
        self.replied_at = timezone.now()
        self.save()


class Event(models.Model):
    """Model for upcoming events"""
    title = models.CharField(max_length=200)
    venue = models.CharField(max_length=200, help_text="Location/venue of the event")
    date = models.DateField()
    time_start = models.TimeField()
    time_end = models.TimeField()
    description = models.TextField(blank=True, help_text="Brief description of the event")
    is_upcoming = models.BooleanField(default=True, help_text="Show this event on the website")
    image = models.ImageField(upload_to='events/', blank=True, null=True, help_text="Event image (optional)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        ordering = ['date']

    def __str__(self):
        return f"{self.title} - {self.date}"

    @property
    def formatted_date(self):
        return self.date.strftime('%B %d, %Y')

    @property
    def formatted_time(self):
        return f"{self.time_start.strftime('%I:%M %p')} - {self.time_end.strftime('%I:%M %p')}"
    
    
    @property
    def get_image_url(self):
        """Return image URL or None if not set"""
        if self.image:
            return self.image.url
        return None