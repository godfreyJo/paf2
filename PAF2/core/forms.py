from django import forms
from django.core.validators import RegexValidator
from django.conf import settings
from .models import Volunteer, DonationItem, Partnership, ContactMessage
import re

# conditional import for reCAPTCHA based on the library used

if not settings.DEBUG:
    from django_recaptcha.fields import ReCaptchaField
    from django_recaptcha.widgets import ReCaptchaV3
else:
    # class to mock reCAPTCHA in development (always valid)
    class ReCaptchaField(forms.Field):
        def __init__(self, *args, **kwargs):
            kwargs['required'] = False  # Make it optional in development
            super().__init__(*args, **kwargs)
        def validate(self, value):
            return True  # Always pass validation in development            

class BaseForm(forms.ModelForm):
    """Base form with common functionality"""
    honeypot = forms.CharField(
        required=False, 
        widget=forms.TextInput(attrs={'style': 'display:none', 'tabindex': '-1', 'autocomplete': 'off'})
    )
    
    # only add captcha in production to avoid issues during development
    if not settings.DEBUG:
        captcha = ReCaptchaField(
            widget=ReCaptchaV3,
            label='',
            required=True,
    )    
    def clean_honeypot(self):
        honeypot = self.cleaned_data.get('honeypot')
        if honeypot:
            raise forms.ValidationError('Spam detected. Please leave this field empty.')
        return honeypot
    
    def clean_captcha(self):
        """reCAPTCHA validation is handled by the field itself"""
        if not settings.DEBUG:
            captcha = self.cleaned_data.get('captcha')
            if not captcha:
                raise forms.ValidationError('Please complete the verification.')
            return captcha
        return 'dev-mode-pass'  # In development, we bypass captcha validation
    
    
     

class VolunteerForm(BaseForm):
    """Enhanced Volunteer Form with database storage and bot protection"""
    
    class Meta:
        model = Volunteer
        fields = ['full_name', 'email', 'phone', 'volunteer_type', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+254 759 707546'
            }),
            'volunteer_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell us about your skills or availability (optional)'
            }),
        }
        labels = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone': 'Phone Number',
            'volunteer_type': 'How would you like to volunteer?',
            'message': 'Additional Information',
        }
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.match(r'^\+?[\d\s-]{10,}$', phone):
            raise forms.ValidationError('Enter a valid phone number (minimum 10 digits)')
        return phone


class DonationItemForm(BaseForm):
    """Enhanced Donation Form with database storage and bot protection"""
    
    class Meta:
        model = DonationItem
        fields = ['donor_name', 'donor_email', 'donor_phone', 'item_category', 'item_description', 'drop_off_date']
        widgets = {
            'donor_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your name'
            }),
            'donor_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com'
            }),
            'donor_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+254 759 707546'
            }),
            'item_category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'item_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe the items (quantity, condition, etc.)'
            }),
            'drop_off_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
        labels = {
            'donor_name': 'Your Name',
            'donor_email': 'Email Address',
            'donor_phone': 'Phone Number',
            'item_category': 'What would you like to donate?',
            'item_description': 'Item Details',
            'drop_off_date': 'Preferred Drop-off Date (optional)',
        }
    
    def clean_phone(self):
        phone = self.cleaned_data.get('donor_phone')
        if not re.match(r'^\+?[\d\s-]{10,}$', phone):
            raise forms.ValidationError('Enter a valid phone number')
        return phone


class PartnershipForm(BaseForm):
    """Enhanced Partnership Form with database storage and bot protection"""
    
    class Meta:
        model = Partnership
        fields = ['organization_name', 'contact_person', 'email', 'phone', 'partner_type', 'proposal']
        widgets = {
            'organization_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Organization name (if applicable)'
            }),
            'contact_person': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contact person name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@organization.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+254 759 707546'
            }),
            'partner_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'proposal': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describe your partnership proposal or sponsorship interest'
            }),
        }
        labels = {
            'organization_name': 'Organization Name',
            'contact_person': 'Contact Person',
            'email': 'Email Address',
            'phone': 'Phone Number',
            'partner_type': 'Partnership Type',
            'proposal': 'Partnership Proposal',
        }
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.match(r'^\+?[\d\s-]{10,}$', phone):
            raise forms.ValidationError('Enter a valid phone number')
        return phone


class ContactForm(BaseForm):
    """Enhanced Contact Form with database storage and bot protection"""
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'inquiry_type', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+254 759 707546'
            }),
            'inquiry_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subject of your message'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Your message...'
            }),
        }
        labels = {
            'name': 'Your Name',
            'email': 'Email Address',
            'phone': 'Phone Number (optional)',
            'inquiry_type': 'Type of Inquiry',
            'subject': 'Subject',
            'message': 'Message',
        }