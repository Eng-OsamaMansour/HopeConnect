from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Campaign, CampaignCategory
from .tasks import notify_new_emergency_campaign
import os
IS_SEEDING = os.environ.get('DJANGO_SEEDING', 'False').lower() == 'true'

@receiver(post_save, sender=Campaign)
def campaign_post_save(sender, instance, created, **kwargs):
    # Skip sending emails during seeding
    if IS_SEEDING:
        return
    try:
        if created and instance.category == CampaignCategory.EMERGENCY:
            notify_new_emergency_campaign.delay(instance.id)
            print("Sent email to all users")
    except Exception as e:
        raise e
