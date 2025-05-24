from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Delivery
import os

# Flag to check if we're in seeding mode
IS_SEEDING = os.environ.get('DJANGO_SEEDING', 'False').lower() == 'true'

@shared_task
def send_delivery_creation_email(delivery_id):
    if IS_SEEDING:
        return
    try:
        delivery = Delivery.objects.get(id=delivery_id)
        
        subject = 'Delivery Created for Your Donation'
        message = f"""
Dear {delivery.donation.donor.get_full_name()},

A delivery has been created for your donation. Here are the delivery details:

Delivery Status: {delivery.get_status_display()}
Pickup Date: {delivery.pickup_date or 'Not set'}
Dropoff Date: {delivery.dropOff_date or 'Not set'}

We will keep you updated on the delivery status. Thank you for your donation.

Best regards,
The HopeConnect Support Team
        """

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [delivery.donation.donor.email],
            fail_silently=False,
        )
        print("Delivery Creation Email Sent to: ", delivery.donation.donor.email)
    except Delivery.DoesNotExist:
        pass

@shared_task
def send_delivery_status_update_email(delivery_id):
    if IS_SEEDING:
        return
    try:
        delivery = Delivery.objects.get(id=delivery_id)

        subject = 'Delivery Status Updated'
        message = f"""
Dear {delivery.donation.donor.get_full_name()},

The status of your donation delivery has been updated.

New Delivery Status: {delivery.get_status_display()}
Pickup Date: {delivery.pickup_date or 'Not set'}
Dropoff Date: {delivery.dropOff_date or 'Not set'}

Thank you for your donation.

Best regards,
The HopeConnect Support Team
        """

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [delivery.donation.donor.email],
            fail_silently=False,
        )
        print("Delivery Status Update Email Sent to: ", delivery.donation.donor.email)
    except Delivery.DoesNotExist:
        pass

@shared_task
def send_delivery_location_update_email(delivery_id):
    if IS_SEEDING:
        return
    try:
        delivery = Delivery.objects.get(id=delivery_id)

        subject = 'Delivery Location Updated'
        message = f"""
Dear {delivery.donation.donor.get_full_name()},

The location of your donation delivery has been updated.    

Current Location: {delivery.current_location.latitude}, {delivery.current_location.longitude}

Thank you for your donation.

Best regards,
The HopeConnect Support Team
        """

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [delivery.donation.donor.email],    
            fail_silently=False,
        )
        print("Delivery Status Update Email Sent to: ", delivery.donation.donor.email)
    except Delivery.DoesNotExist:
        pass


