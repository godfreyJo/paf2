from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.conf import settings
from .forms import ContactForm
from django.utils import timezone
from .models import ContactMessage, Event
import traceback
import logging

logger = logging.getLogger(__name__)


def home(request):
    """Home page view with all sections."""
    context = {
        'title': 'Phidelis Ann Foundation - Empower Them Today',
        'stats': {
            'children': 200,
            'schools': 5,
            'communities': 8,
        },
        'mission_items': [
            {
                'icon': 'book-open',
                'title': 'Education Access',
                'description': 'Textbooks, stationery, uniforms — removing learning barriers'
            },
            {
                'icon': 'heart',
                'title': 'Girl Child Support',
                'description': 'Sanitary pads, mentorship, dignity for girls to stay in school'
            },
            {
                'icon': 'users',
                'title': 'Community Outreach',
                'description': 'Direct events, volunteer drives, local partnerships in Kakamega'
            },
            {
                'icon': 'sparkles',
                'title': 'Health & Hygiene',
                'description': 'Undergarments, hygiene education, personal care essentials'
            },
        ],
        'approach_items': [
            {
                'icon': 'hand-heart',
                'title': 'Dignity-first support',
                'description': 'Every child deserves respect and confidence. We ensure that our support maintains and uplifts the dignity of every learner we serve.'
            },
            {
                'icon': 'users',
                'title': 'Community involvement',
                'description': 'Working with local leaders, schools, and families to ensure our interventions are relevant, accepted, and sustainable.'
            },
            {
                'icon': 'graduation-cap',
                'title': 'Sustainable impact',
                'description': 'Creating long-term change, not just short-term aid. We focus on solutions that continue to benefit communities for years to come.'
            },
        ],
        'gallery_images': [
            {
                'src': 'main/images/community_outreach.jpg',
                'title': 'Community Outreach',
                'description': 'Distributing school supplies to children in Kakamega'
            },
            {
                'src': 'main/images/children_studying_together.jpg',
                'title': 'Learning Together',
                'description': 'Creating spaces for collaborative learning and growth'
            },
        ],
    }
    return render(request, 'main/index.html', context)


def about(request):
    """About page view."""
    context = {
        'title': 'About Us - Phidelis Ann Foundation',
    }
    return render(request, 'main/about.html', context)


def programs(request):

     # Get upcoming events
    upcoming_events = Event.objects.filter(is_upcoming=True).order_by('date')
    """Programs page view."""
    context = {
        'title': 'Our Programs - Phidelis Ann Foundation',
        'programs': [
            {
                'title': 'Education Access Program',
                'description': 'Providing textbooks, stationery, and uniforms to remove learning barriers.',
                'image': 'main/images/school_supplies.jpg',
            },
            {
                'title': 'Girl Child Support',
                'description': 'Mentorship, sanitary pads, and dignity kits to keep girls in school.',
                'image': 'main/images/girls_mentorship.jpg',
            },
            {
                'title': 'Health & Hygiene',
                'description': 'Hygiene education and personal care essentials for healthy living.',
                'image': 'main/images/hygiene_education.jpg',
            },
            {
                'title': 'Community Outreach',
                'description': 'Direct events and volunteer drives in Kakamega communities.',
                'image': 'main/images/uniform_distribution.jpg',
            },
        ],
        'upcoming_events': upcoming_events,  
    }

    
    return render(request, 'main/programs.html', context)


def gallery(request):
    """Gallery page view with all images."""
    context = {
        'title': 'Gallery - Phidelis Ann Foundation',
        'images': [
            {
                'src': 'main/images/hero_children_classroom.jpg',
                'title': 'Classroom Learning',
                'category': 'Education'
            },
            {
                'src': 'main/images/girl_child_education.jpg',
                'title': 'Girl Child Education',
                'category': 'Education'
            },
            {
                'src': 'main/images/community_outreach.jpg',
                'title': 'Community Outreach',
                'category': 'Outreach'
            },
            {
                'src': 'main/images/children_studying_together.jpg',
                'title': 'Group Study Session',
                'category': 'Education'
            },
            {
                'src': 'main/images/uniform_distribution.jpg',
                'title': 'Uniform Distribution',
                'category': 'Outreach'
            },
            {
                'src': 'main/images/girls_mentorship.jpg',
                'title': 'Girls Mentorship Program',
                'category': 'Mentorship'
            },
            {
                'src': 'main/images/hygiene_education.jpg',
                'title': 'Hygiene Education',
                'category': 'Health'
            },
            {
                'src': 'main/images/kakamega_village.jpg',
                'title': 'Kakamega Community',
                'category': 'Community'
            },
            {
                'src': 'main/images/school_supplies.jpg',
                'title': 'School Supplies',
                'category': 'Education'
            },
            {
                'src': 'main/images/teacher_portrait.jpg',
                'title': 'Our Teachers',
                'category': 'Education'
            },
            {
                'src': 'main/images/children_playing.jpg',
                'title': 'Children at Play',
                'category': 'Community'
            },
            {
                'src': 'main/images/volunteer_packing.jpg',
                'title': 'Volunteer Activities',
                'category': 'Volunteer'
            },
        ],
    }
    return render(request, 'main/gallery.html', context)

def contact(request):
    """Contact page view with form handling."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                # Save to database
                contact = form.save()
                print(f"✓ Contact saved to database - ID: {contact.id}")
                print(f"  - Name: {contact.first_name} {contact.last_name}")
                print(f"  - Email: {contact.email}")
                
                # Get subject display value
                subject_display = dict(ContactMessage.INQUIRY_TYPES).get(contact.subject, contact.subject)
                
                email_sent = False
                
                # Send auto-reply to user
                try:
                    subject = f'Thank you for contacting Phidelis Ann Foundation'
                    message = f"""Dear {contact.first_name},

Thank you for contacting Phidelis Ann Foundation. We have received your message and will get back to you within 2-3 business days.

Your Inquiry Details:
- Type: {subject_display}
- Message: {contact.message[:200]}...

If your matter is urgent, please call us at +254 759 707546.

Best regards,
Phidelis Ann Foundation Team

---
Phidelis Ann Foundation | Empowering communities through education and dignity
Website: {settings.SITE_URL}
Contact: {settings.CONTACT_EMAIL} | +254 759 707546
"""
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [contact.email],
                        fail_silently=False,
                    )
                    print(f"✓ Auto-reply sent to {contact.email}")
                    email_sent = True
                    
                except Exception as email_error:
                    print(f"✗ Error sending auto-reply: {email_error}")
                    print(traceback.format_exc())
                
                # Send notification to admin
                try:
                    admin_subject = f'New Contact Form: {contact.first_name} {contact.last_name}'
                    admin_message = f"""New message received from {contact.first_name} {contact.last_name}

Subject: {subject_display}
Email: {contact.email}

Message:
{contact.message}

Submitted: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}

View in admin: {settings.SITE_URL}/admin/main/contactmessage/{contact.id}/change/

Action Required: Please respond to this inquiry within 2-3 business days.
"""
                    send_mail(
                        admin_subject,
                        admin_message,
                        settings.DEFAULT_FROM_EMAIL,
                        [settings.ADMIN_EMAIL],
                        fail_silently=False,
                    )
                    print(f"✓ Admin notification sent to {settings.ADMIN_EMAIL}")
                except Exception as admin_error:
                    print(f"✗ Error sending admin notification: {admin_error}")
                
                # Set success message
                if email_sent:
                    messages.success(request, f'✓ Your {subject_display} inquiry has been sent successfully! We will get back to you soon.')
                else:
                    messages.warning(request, f'✓ Your {subject_display} inquiry was saved. We will contact you directly.')
                
                # Redirect back to contact page with a flag to scroll to messages
                # Use session to indicate form was just submitted
                request.session['form_submitted'] = True
                return redirect('contact')
                
            except Exception as db_error:
                print(f"✗ Database error: {db_error}")
                print(traceback.format_exc())
                messages.error(request, 'There was an error saving your message. Please try again or call us directly.')
                # Keep form data on error
                return render(request, 'main/contact.html', {
                    'title': 'Contact Us - Phidelis Ann Foundation',
                    'form': form,
                })
        else:
            print(f"✗ Contact form is invalid")
            print(f"Form errors: {form.errors}")
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
            # Keep form data on validation error
            return render(request, 'main/contact.html', {
                'title': 'Contact Us - Phidelis Ann Foundation',
                'form': form,
            })
    else:
        # Check if we just submitted a form (clear form on success)
        if request.session.pop('form_submitted', False):
            # Return empty form after successful submission
            form = ContactForm()
        else:
            form = ContactForm()
    
    context = {
        'title': 'Contact Us - Phidelis Ann Foundation',
        'form': form,
        'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY, 
    }
    return render(request, 'main/contact.html', context)

