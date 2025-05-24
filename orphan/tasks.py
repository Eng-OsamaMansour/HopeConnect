from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import OrphanUpdate
from django.db.models.signals import post_save
from django.dispatch import receiver
import os

# Flag to check if we're in seeding mode
IS_SEEDING = os.environ.get('DJANGO_SEEDING', 'False').lower() == 'true'

@shared_task
def notify_sponsor_of_update(update_id):
    if IS_SEEDING:
        return
    try:
        update = OrphanUpdate.objects.get(id=update_id)
        
        subject = f'Update about {update.orphan.name}'
        message = f"""
Dear {update.orphan.sponsor.get_full_name()},

We have an update about {update.orphan.name}:

{update.content}

Update Details:
- Type: {update.get_update_type_display()}
- Date: {update.created_at.strftime('%B %d, %Y')}

Thank you for your continued support.

Best regards,
The HopeConnect Support Team
        """

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [update.orphan.sponsor.email],
            fail_silently=False,
        )
        print("Sponsor Update Email Sent to: ", update.orphan.sponsor.email)
    except OrphanUpdate.DoesNotExist:
        pass

