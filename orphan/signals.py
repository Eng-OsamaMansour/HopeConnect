from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OrphanUpdate
from .tasks import notify_sponsor_of_update
import os

IS_SEEDING = os.environ.get('DJANGO_SEEDING', 'False').lower() == 'true'

@receiver(post_save, sender=OrphanUpdate)
def orphan_update_post_save(sender, instance, created, **kwargs):
    # Skip sending emails during seeding
    if IS_SEEDING:
        return
        
    try:
        if created and instance.orphan.sponsor:
            notify_sponsor_of_update.delay(instance.id)
    except Exception as e:
        raise e