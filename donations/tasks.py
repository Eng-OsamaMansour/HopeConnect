from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Donation, DonationReport
import os

# Flag to check if we're in seeding mode
IS_SEEDING = os.environ.get('DJANGO_SEEDING', 'False').lower() == 'true'

@shared_task
def send_donation_confirmation_email(donation_id):
    if IS_SEEDING:
        return
    try:
        donation = Donation.objects.get(id=donation_id)
        
        subject = 'Thank you for your donation!'
        
        if donation.donation_type == 'ORPHAN':
            message = f"""
Dear {donation.donor.get_full_name()},

Thank you for your generous donation to help {donation.orphan.name}. Your support means the world to us and will make a real difference in their life.

Donation Details:
- Category: {donation.get_donation_category_display()}
- Status: {donation.get_status_display()}
- Date: {donation.created_at.strftime('%B %d, %Y')}

We will keep you updated on how your donation is helping. Thank you again for your kindness and generosity.

Best regards,
The HopeConnect Support Team
            """
        else:
            message = f"""
Dear {donation.donor.get_full_name()},

Thank you for your generous donation to our {donation.get_donation_type_display()} campaign. Your support helps us make a difference in children's lives.

Donation Details:
- Category: {donation.get_donation_category_display()}
- Status: {donation.get_status_display()} 
- Date: {donation.created_at.strftime('%B %d, %Y')}

We will keep you updated on the impact of your donation. Thank you again for your support.

Best regards,
The HopeConnect Support Team
            """

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [donation.donor.email],
            fail_silently=False,
        )
        print("Donation Confirmation Email Sent to: ", donation.donor.email)
    except Donation.DoesNotExist:
        pass

@shared_task 
def send_donation_status_update_email(donation_id):
    if IS_SEEDING:
        return
    try:
        donation = Donation.objects.get(id=donation_id)

        subject = 'Your Donation Status Has Been Updated'
        message = f"""
Dear {donation.donor.get_full_name()},

We wanted to let you know that the status of your donation has been updated.

New Status: {donation.get_status_display()}

Donation Details:
- Category: {donation.get_donation_category_display()}
- Type: {donation.get_donation_type_display()}
- Date: {donation.created_at.strftime('%B %d, %Y')}

Thank you again for your generous support. If you have any questions, please don't hesitate to contact us.

Best regards,
The HopeConnect Support Team
        """

        send_mail(
            subject,
            message, 
            settings.DEFAULT_FROM_EMAIL,
            [donation.donor.email],
            fail_silently=False,
        )
        print("Donation Status Update Email Sent to: ", donation.donor.email)
    except Donation.DoesNotExist:
        pass

@receiver(post_save, sender=Donation)
def donation_post_save(sender, instance, created, **kwargs):
    # Skip sending emails during seeding
    if IS_SEEDING:
        return
        
    try:
        if created:
            send_donation_confirmation_email.delay(instance.id)
        else:
            # Only send status update email if status field was changed
            if instance.tracker.has_changed('status'):
                send_donation_status_update_email.delay(instance.id)
    except Exception:
        # If Celery is not running, just skip sending the email
        pass

@shared_task
def send_donation_report_email(report_id):
    if IS_SEEDING:
        return
    try:
        report = DonationReport.objects.get(id=report_id)
        donation = report.donation

        subject = 'New Report for Your Donation'
        message = f"""
Dear {donation.donor.get_full_name()},

A new report has been created for your donation.

Donation Details:
- Category: {donation.get_donation_category_display()}
- Type: {donation.get_donation_type_display()} 
- Date: {donation.created_at.strftime('%B %d, %Y')}

Report:
{report.report}

Thank you for your continued support.

Best regards,
The HopeConnect Support Team
        """

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [donation.donor.email],
            fail_silently=False,
        )
        print("Donation Report Email Sent to: ", donation.donor.email)          
    except DonationReport.DoesNotExist:
        pass

@receiver(post_save, sender=DonationReport)
def donation_report_post_save(sender, instance, created, **kwargs):
    # Skip sending emails during seeding
    if IS_SEEDING:
        return
                
    try:
        if created:
            send_donation_report_email.delay(instance.id)
    except Exception:
        # If Celery is not running, just skip sending the email
        pass