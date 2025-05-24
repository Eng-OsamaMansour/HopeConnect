from django.db.models.signals import post_save
from django.dispatch import receiver
from orphanages.models import OrphanageNeedRequest
from volunteers.models import VolunteerOfferRequest
from .tasks import run_semantic_matching

@receiver(post_save, sender=OrphanageNeedRequest)
@receiver(post_save, sender=VolunteerOfferRequest)
def kick_matcher(sender, instance, created, **kwargs):
    if instance.embedding:  # only run matcher if embedding is already set
        print(f"✅ Signal triggered for {sender.__name__}")
        run_semantic_matching.delay()

