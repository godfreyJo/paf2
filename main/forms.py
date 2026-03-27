from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.fields import ReCaptchaV3
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    """Contact form for inquiries with reCAPTCHA"""
    
    # Add reCAPTCHA field
    captcha = ReCaptchaField(
        widget=ReCaptchaV3,
        label='',
        required=True,
    )
    
    class Meta:
        model = ContactMessage
        fields = ['first_name', 'last_name', 'email', 'subject', 'message']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-paf-beige rounded-lg focus:outline-none focus:border-paf-gold transition-colors',
                'placeholder': 'Your first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-paf-beige rounded-lg focus:outline-none focus:border-paf-gold transition-colors',
                'placeholder': 'Your last name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-paf-beige rounded-lg focus:outline-none focus:border-paf-gold transition-colors',
                'placeholder': 'your@email.com'
            }),
            'subject': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-paf-beige rounded-lg focus:outline-none focus:border-paf-gold transition-colors'
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-paf-beige rounded-lg focus:outline-none focus:border-paf-gold transition-colors resize-none',
                'rows': 5,
                'placeholder': 'Your message...'
            }),
        }
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'subject': 'Subject',
            'message': 'Message',
        }