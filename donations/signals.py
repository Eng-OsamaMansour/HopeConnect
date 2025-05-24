from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DonationReport
from .tasks import send_donation_report_email
import os

IS_SEEDING = os.environ.get('DJANGO_SEEDING', 'False').lower() == 'true'

@receiver(post_save, sender=DonationReport)
def donation_report_post_save(sender, instance, created, **kwargs):
    # Skip sending emails during seeding
    if IS_SEEDING:
        return
                
    try:
        if created:
            send_donation_report_email.delay(instance.id)
    except Exception as e:
        raise e