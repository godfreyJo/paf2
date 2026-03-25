from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .forms import VolunteerForm, DonationItemForm, PartnershipForm, ContactForm
from .models import Volunteer, DonationItem, Partnership, ContactMessage
import logging
import traceback

logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')

def join(request):
    volunteer_form = VolunteerForm()
    donation_form = DonationItemForm()
    partnership_form = PartnershipForm()
    
    if request.method == 'POST':
        print(f"\n{'='*60}")
        print(f"POST Request Received at {timezone.now()}")
        print(f"POST keys: {list(request.POST.keys())}")
        print(f"Form Type: {request.POST.get('form_type', 'Not found')}")
        print(f"{'='*60}\n")

        # Get the form type from the hidden field
        form_type = request.POST.get('form_type')
        
        # Handle Volunteer Form
        if form_type == 'volunteer':
            print(">>> Processing Volunteer Form")
            volunteer_form = VolunteerForm(request.POST)
            
            if volunteer_form.is_valid():
                print("✓ Volunteer form is valid")
                try:
                    # Save to database
                    volunteer = volunteer_form.save()
                    print(f"✓ Volunteer saved to database - ID: {volunteer.id}")
                    print(f"  - Name: {volunteer.full_name}")
                    print(f"  - Email: {volunteer.email}")
                    print(f"  - Type: {volunteer.volunteer_type}")
                    
                    # Track if any email was sent
                    email_sent = False
                    
                    # Send confirmation email to volunteer
                    try:
                        print("Attempting to send confirmation email to volunteer...")
                        
                        # Get display value for volunteer type
                        volunteer_type_display = dict(Volunteer.VOLUNTEER_TYPES).get(
                            volunteer.volunteer_type, volunteer.volunteer_type
                        )
                        
                        subject = 'Thank you for volunteering with Phidelis Ann Foundation'
                        message = f"""Dear {volunteer.full_name},

Thank you for your interest in volunteering with Phidelis Ann Foundation! We have received your application.

Your Details:
- Volunteer Type: {volunteer_type_display}
- Email: {volunteer.email}
- Phone: {volunteer.phone}
- Message: {volunteer.message or 'Not provided'}

Our upcoming outreach is on May 8th, 2026 at Emalindi Mixed Secondary, Khwisero.

We will contact you soon with more details. In the meantime, feel free to reach out if you have any questions.

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
                            [volunteer.email],
                            fail_silently=False,
                        )
                        print(f"✓ Confirmation email sent to {volunteer.email}")
                        email_sent = True
                        
                    except Exception as email_error:
                        print(f"✗ Error sending confirmation email: {email_error}")
                        print(traceback.format_exc())
                    
                    # Send notification email to admin
                    try:
                        print("Attempting to send admin notification...")
                        admin_email = getattr(settings, 'ADMIN_EMAIL', settings.DEFAULT_FROM_EMAIL)
                        volunteer_type_display = dict(Volunteer.VOLUNTEER_TYPES).get(
                            volunteer.volunteer_type, volunteer.volunteer_type
                        )
                        
                        admin_subject = f'New Volunteer Application: {volunteer.full_name}'
                        admin_message = f"""New volunteer application received!

Name: {volunteer.full_name}
Email: {volunteer.email}
Phone: {volunteer.phone}
Volunteer Type: {volunteer_type_display}
Message: {volunteer.message or 'No message provided'}

Submitted: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}

View in admin: {settings.SITE_URL}/admin/core/volunteer/{volunteer.id}/change/

Action Required: Please follow up with this volunteer within 2-3 business days.
"""
                        send_mail(
                            admin_subject,
                            admin_message,
                            settings.DEFAULT_FROM_EMAIL,
                            [admin_email],
                            fail_silently=False,
                        )
                        print(f"✓ Admin notification sent to {admin_email}")
                    except Exception as admin_error:
                        print(f"✗ Error sending admin notification: {admin_error}")
                        print(traceback.format_exc())
                    
                    # Set success message based on email status
                    if email_sent:
                        messages.success(request, 'Thank you for volunteering! Check your email for confirmation.')
                    else:
                        messages.warning(request, 'Your application was saved successfully, but we could not send a confirmation email. We will contact you directly.')
                    
                    return redirect('join')
                    
                except Exception as db_error:
                    print(f"✗ Database error: {db_error}")
                    print(traceback.format_exc())
                    messages.error(request, 'There was an error saving your application. Please try again or contact us directly.')
            else:
                print(f"✗ Volunteer form is invalid")
                print(f"Form errors: {volunteer_form.errors}")
                for field, errors in volunteer_form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
        
        # Handle Donation Form
        elif form_type == 'donation':
            print(">>> Processing Donation Form")
            donation_form = DonationItemForm(request.POST)
            
            if donation_form.is_valid():
                print("✓ Donation form is valid")
                try:
                    # Save to database
                    donation = donation_form.save()
                    print(f"✓ Donation saved to database - ID: {donation.id}")
                    print(f"  - Donor: {donation.donor_name}")
                    print(f"  - Email: {donation.donor_email}")
                    print(f"  - Category: {donation.item_category}")
                    
                    email_sent = False
                    
                    # Send confirmation to donor
                    try:
                        print("Attempting to send confirmation email to donor...")
                        
                        category_display = dict(DonationItem.ITEM_CATEGORIES).get(
                            donation.item_category, donation.item_category
                        )
                        
                        subject = 'Thank you for your donation - Phidelis Ann Foundation'
                        message = f"""Dear {donation.donor_name},

Thank you for your generosity! We have received your donation offer.

Donation Details:
- Category: {category_display}
- Description: {donation.item_description}
- Drop-off Date: {donation.drop_off_date or 'To be arranged'}

We will contact you shortly to coordinate the drop-off. If you have any questions, please don't hesitate to reach out.

Thank you for making a difference in our community!

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
                            [donation.donor_email],
                            fail_silently=False,
                        )
                        print(f"✓ Confirmation email sent to {donation.donor_email}")
                        email_sent = True
                        
                    except Exception as email_error:
                        print(f"✗ Error sending confirmation email: {email_error}")
                        print(traceback.format_exc())
                    
                    # Send notification to admin
                    try:
                        print("Attempting to send admin notification...")
                        admin_email = getattr(settings, 'ADMIN_EMAIL', settings.DEFAULT_FROM_EMAIL)
                        category_display = dict(DonationItem.ITEM_CATEGORIES).get(
                            donation.item_category, donation.item_category
                        )
                        
                        admin_subject = f'New Donation Offer: {donation.donor_name}'
                        admin_message = f"""New donation offer received!

Donor: {donation.donor_name}
Email: {donation.donor_email}
Phone: {donation.donor_phone}
Category: {category_display}
Description: {donation.item_description}
Drop-off Date: {donation.drop_off_date or 'Not specified'}

View in admin: {settings.SITE_URL}/admin/core/donationitem/{donation.id}/change/

Action Required: Please contact donor to arrange drop-off within 2-3 business days.
"""
                        send_mail(
                            admin_subject,
                            admin_message,
                            settings.DEFAULT_FROM_EMAIL,
                            [admin_email],
                            fail_silently=False,
                        )
                        print(f"✓ Admin notification sent to {admin_email}")
                    except Exception as admin_error:
                        print(f"✗ Error sending admin notification: {admin_error}")
                    
                    if email_sent:
                        messages.success(request, 'Thank you for your donation! We will contact you soon.')
                    else:
                        messages.warning(request, 'Donation recorded, but we could not send confirmation email. We will contact you directly.')
                    
                    return redirect('join')
                    
                except Exception as db_error:
                    print(f"✗ Database error: {db_error}")
                    print(traceback.format_exc())
                    messages.error(request, 'There was an error saving your donation. Please try again.')
            else:
                print(f"✗ Donation form is invalid")
                print(f"Form errors: {donation_form.errors}")
                for field, errors in donation_form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
        
        # Handle Partnership Form
        elif form_type == 'partnership':
            print(">>> Processing Partnership Form")
            partnership_form = PartnershipForm(request.POST)
            
            if partnership_form.is_valid():
                print("✓ Partnership form is valid")
                try:
                    # Save to database
                    partnership = partnership_form.save()
                    print(f"✓ Partnership saved to database - ID: {partnership.id}")
                    print(f"  - Contact: {partnership.contact_person}")
                    print(f"  - Email: {partnership.email}")
                    print(f"  - Type: {partnership.partner_type}")
                    
                    email_sent = False
                    
                    # Send confirmation email
                    try:
                        print("Attempting to send confirmation email...")
                        
                        partner_type_display = dict(Partnership.PARTNER_TYPES).get(
                            partnership.partner_type, partnership.partner_type
                        )
                        
                        subject = 'Partnership Inquiry Received - Phidelis Ann Foundation'
                        message = f"""Dear {partnership.contact_person},

Thank you for your interest in partnering with Phidelis Ann Foundation!

Partnership Details:
- Type: {partner_type_display}
- Organization: {partnership.organization_name or 'Individual'}

We have received your proposal and will review it carefully. Our team will contact you within 3-5 business days to discuss next steps.

If you have any additional information to share, please feel free to reply to this email.

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
                            [partnership.email],
                            fail_silently=False,
                        )
                        print(f"✓ Confirmation email sent to {partnership.email}")
                        email_sent = True
                        
                    except Exception as email_error:
                        print(f"✗ Error sending confirmation email: {email_error}")
                        print(traceback.format_exc())
                    
                    # Send notification to admin
                    try:
                        print("Attempting to send admin notification...")
                        admin_email = getattr(settings, 'ADMIN_EMAIL', settings.DEFAULT_FROM_EMAIL)
                        partner_type_display = dict(Partnership.PARTNER_TYPES).get(
                            partnership.partner_type, partnership.partner_type
                        )
                        
                        admin_subject = f'New Partnership Inquiry: {partnership.contact_person}'
                        admin_message = f"""New partnership inquiry received!

Contact Person: {partnership.contact_person}
Organization: {partnership.organization_name or 'Individual'}
Type: {partner_type_display}
Email: {partnership.email}
Phone: {partnership.phone}

Proposal:
{partnership.proposal}

View in admin: {settings.SITE_URL}/admin/core/partnership/{partnership.id}/change/

Action Required: Review proposal and respond within 3-5 business days.
"""
                        send_mail(
                            admin_subject,
                            admin_message,
                            settings.DEFAULT_FROM_EMAIL,
                            [admin_email],
                            fail_silently=False,
                        )
                        print(f"✓ Admin notification sent to {admin_email}")
                    except Exception as admin_error:
                        print(f"✗ Error sending admin notification: {admin_error}")
                    
                    if email_sent:
                        messages.success(request, 'Thank you for your partnership inquiry! We will contact you soon.')
                    else:
                        messages.warning(request, 'Inquiry saved, but we could not send confirmation email. We will contact you directly.')
                    
                    return redirect('join')
                    
                except Exception as db_error:
                    print(f"✗ Database error: {db_error}")
                    print(traceback.format_exc())
                    messages.error(request, 'There was an error saving your inquiry. Please try again.')
            else:
                print(f"✗ Partnership form is invalid")
                print(f"Form errors: {partnership_form.errors}")
                for field, errors in partnership_form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
        else:
            print(f"⚠ Unknown form type: {form_type}")
            messages.error(request, 'Form submission error. Please try again.')
    
    context = {
        'volunteer_form': volunteer_form,
        'donation_form': donation_form,
        'partnership_form': partnership_form,
        'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY,
    }
    return render(request, 'core/join.html', context)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                # Save to database
                contact = form.save()
                print(f"✓ Contact saved to database - ID: {contact.id}")
                print(f"  - Name: {contact.name}")
                print(f"  - Email: {contact.email}")
                
                email_sent = False
                
                # Send auto-reply to user
                try:
                    print("Attempting to send auto-reply...")
                    
                    inquiry_type_display = dict(ContactMessage.INQUIRY_TYPES).get(
                        contact.inquiry_type, contact.inquiry_type
                    )
                    
                    subject = 'We received your message - Phidelis Ann Foundation'
                    message = f"""Dear {contact.name},

Thank you for contacting Phidelis Ann Foundation. We have received your message and will get back to you within 2-3 business days.

Your Inquiry Details:
- Type: {inquiry_type_display}
- Subject: {contact.subject}
- Message Preview: {contact.message[:200]}...

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
                    print("Attempting to send admin notification...")
                    admin_email = getattr(settings, 'ADMIN_EMAIL', settings.DEFAULT_FROM_EMAIL)
                    inquiry_type_display = dict(ContactMessage.INQUIRY_TYPES).get(
                        contact.inquiry_type, contact.inquiry_type
                    )
                    
                    admin_subject = f'New Contact Form: {contact.subject}'
                    admin_message = f"""New message received from {contact.name}

Inquiry Type: {inquiry_type_display}
Email: {contact.email}
Phone: {contact.phone or 'Not provided'}
Subject: {contact.subject}

Message:
{contact.message}

Submitted: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}

View in admin: {settings.SITE_URL}/admin/core/contactmessage/{contact.id}/change/

Action Required: Please respond to this inquiry within 2-3 business days.
"""
                    send_mail(
                        admin_subject,
                        admin_message,
                        settings.DEFAULT_FROM_EMAIL,
                        [admin_email],
                        fail_silently=False,
                    )
                    print(f"✓ Admin notification sent to {admin_email}")
                except Exception as admin_error:
                    print(f"✗ Error sending admin notification: {admin_error}")
                
                if email_sent:
                    messages.success(request, 'Your message has been sent. We will get back to you soon!')
                else:
                    messages.warning(request, 'Message saved, but we could not send confirmation. We will still respond to your inquiry.')
                
                return redirect('contact')
                
            except Exception as db_error:
                print(f"✗ Database error: {db_error}")
                print(traceback.format_exc())
                messages.error(request, 'There was an error saving your message. Please try again or call us directly.')
        else:
            print(f"✗ Contact form is invalid")
            print(f"Form errors: {form.errors}")
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
        'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY,
    }
    return render(request, 'core/contact.html', context)

def events(request):
    """Display upcoming events"""
    try:
        from .models import OutreachEvent
        upcoming_events = OutreachEvent.objects.filter(is_upcoming=True).order_by('date')
        return render(request, 'core/events.html', {'events': upcoming_events})
    except:
        return render(request, 'core/events.html', {'events': []})