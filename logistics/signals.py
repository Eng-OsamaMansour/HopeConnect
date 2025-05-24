from django.db.models.signals import post_save
from .models import Delivery
from .tasks import send_delivery_creation_email, send_delivery_status_update_email, send_delivery_location_update_email
from django.dispatch import receiver
import os
IS_SEEDING = os.environ.get('DJANGO_SEEDING', 'False').lower() == 'true'


@receiver(post_save, sender=Delivery)
def delivery_post_save(sender, instance, created, **kwargs):
    # Skip sending emails during seeding
    if IS_SEEDING:
        return        
    try:
        if created:
            send_delivery_creation_email.delay(instance.id)
        else:
            if instance.tracker.has_changed('status'):
                send_delivery_status_update_email.delay(instance.id)
            if instance.tracker.has_changed('current_location'):
                send_delivery_location_update_email.delay(instance.id)
    except Exception as e:
        raise e