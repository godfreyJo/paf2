from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone


class Volunteer(models.Model):
    """Model to store volunteer applications"""
    
    # Choices for volunteer type
    VOLUNTEER_TYPES = [
        ('event', 'Event Volunteer (May 8th)'),
        ('preparation', 'Preparation/Sorting'),
        ('remote', 'Remote Support'),
        ('regular', 'Regular Volunteer'),
    ]
    
    # Status choices for tracking
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('contacted', 'Contacted'),
        ('confirmed', 'Confirmed'),
        ('attended', 'Attended'),
        ('declined', 'Declined'),
    ]
    
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(
        max_length=20,
        validators=[RegexValidator(r'^\+?[\d\s-]{10,}$', 'Enter a valid phone number')]
    )
    volunteer_type = models.CharField(max_length=50, choices=VOLUNTEER_TYPES)
    message = models.TextField(blank=True, help_text="Skills, availability, or special requests")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, help_text="Internal notes about this volunteer")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_contacted = models.BooleanField(default=False)  # Keeping for backward compatibility

    class Meta:
        verbose_name = 'Volunteer Application'
        verbose_name_plural = 'Volunteer Applications'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.get_volunteer_type_display()}"
    
    @property
    def is_active(self):
        """Check if volunteer is still active"""
        return self.status in ['pending', 'contacted', 'confirmed']


class DonationItem(models.Model):
    """Model to store donation items"""
    
    # Item categories
    ITEM_CATEGORIES = [
        ('stationery', 'Stationery & Books'),
        ('uniforms', 'School Uniforms'),
        ('shoes', 'Shoes'),
        ('sanitary', 'Sanitary Pads'),
        ('undergarments', 'Undergarments'),
        ('hygiene', 'Hygiene Products'),
        ('other', 'Other Items'),
    ]
    
    # Status choices
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('contacted', 'Contacted'),
        ('received', 'Received'),
        ('distributed', 'Distributed'),
        ('declined', 'Declined'),
    ]
    
    donor_name = models.CharField(max_length=100)
    donor_email = models.EmailField()
    donor_phone = models.CharField(
        max_length=20,
        validators=[RegexValidator(r'^\+?[\d\s-]{10,}$', 'Enter a valid phone number')]
    )
    item_category = models.CharField(max_length=50, choices=ITEM_CATEGORIES)
    item_description = models.TextField(help_text="Quantity, condition, etc.")
    quantity = models.PositiveIntegerField(null=True, blank=True, help_text="Approximate quantity")
    drop_off_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, help_text="Internal notes about this donation")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Donation Offer'
        verbose_name_plural = 'Donation Offers'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.donor_name} - {self.get_item_category_display()}"


class Partnership(models.Model):
    """Model to store partnership inquiries"""
    
    # Partner types
    PARTNER_TYPES = [
        ('individual', 'Individual Sponsor'),
        ('corporate', 'Corporate/Organization'),
        ('school', 'School/Institution'),
        ('ngo', 'NGO/Non-profit'),
        ('government', 'Government Agency'),
        ('other', 'Other'),
    ]
    
    # Status choices
    STATUS_CHOICES = [
        ('new', 'New Inquiry'),
        ('reviewing', 'Under Review'),
        ('meeting', 'Meeting Scheduled'),
        ('negotiating', 'Negotiating'),
        ('partnered', 'Partnered'),
        ('declined', 'Declined'),
    ]
    
    organization_name = models.CharField(max_length=200, blank=True, help_text="Leave blank if individual")
    contact_person = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(
        max_length=20,
        validators=[RegexValidator(r'^\+?[\d\s-]{10,}$', 'Enter a valid phone number')]
    )
    partner_type = models.CharField(max_length=50, choices=PARTNER_TYPES)
    proposal = models.TextField(help_text="Describe partnership proposal or interest")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    notes = models.TextField(blank=True, help_text="Internal notes about this partnership")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Partnership Inquiry'
        verbose_name_plural = 'Partnership Inquiries'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.contact_person} - {self.get_partner_type_display()}"


class ContactMessage(models.Model):
    """Model to store contact form messages"""
    
    # Inquiry types
    INQUIRY_TYPES = [
        ('general', 'General Inquiry'),
        ('volunteer', 'Volunteering'),
        ('donation', 'Donation'),
        ('partnership', 'Partnership'),
        ('media', 'Media/Press'),
        ('complaint', 'Complaint'),
        ('feedback', 'Feedback'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    inquiry_type = models.CharField(max_length=50, choices=INQUIRY_TYPES)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    reply = models.TextField(blank=True, help_text="Staff reply to this message")
    replied_by = models.CharField(max_length=100, blank=True)
    replied_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_replied = models.BooleanField(default=False)  # Keeping for backward compatibility

    class Meta:
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"
    
    def mark_as_replied(self, staff_name):
        """Mark message as replied"""
        self.is_replied = True
        self.replied_by = staff_name
        self.replied_at = timezone.now()
        self.save()


class NewsletterSubscriber(models.Model):
    """Optional: For email newsletter signups"""
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, blank=True, help_text="Optional")
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Newsletter Subscriber'
        verbose_name_plural = 'Newsletter Subscribers'
        ordering = ['-subscribed_at']
    
    def __str__(self):
        return self.email


class OutreachEvent(models.Model):
    """Optional: For managing outreach events"""
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    date = models.DateField()
    time_start = models.TimeField()
    time_end = models.TimeField()
    description = models.TextField(blank=True)
    is_upcoming = models.BooleanField(default=True)
    volunteers_needed = models.PositiveIntegerField(default=0)
    volunteers_confirmed = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Outreach Event'
        verbose_name_plural = 'Outreach Events'
        ordering = ['date']
    
    def __str__(self):
        return f"{self.title} - {self.date}"
    
    @property
    def volunteers_remaining(self):
        """Calculate remaining volunteer spots"""
        return max(0, self.volunteers_needed - self.volunteers_confirmed)


class EventAttendance(models.Model):
    """Optional: Track volunteer attendance at events"""
    event = models.ForeignKey(OutreachEvent, on_delete=models.CASCADE, related_name='attendees')
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE, related_name='events_attended')
    attended = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['event', 'volunteer']
        verbose_name = 'Event Attendance'
        verbose_name_plural = 'Event Attendances'
    
    def __str__(self):
        return f"{self.volunteer.full_name} - {self.event.title}"