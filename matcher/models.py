from django.db import models
from orphanages.models import OrphanageNeedRequest
from volunteers.models import VolunteerOfferRequest

class OfferStatus(models.TextChoices):
    OPEN = "OPEN"
    MATCHED = "MATCHED"
    CLOSED = "CLOSED"

class Matcher(models.Model):
    need_request = models.ForeignKey(OrphanageNeedRequest, on_delete=models.CASCADE)
    volunteer_offer = models.ForeignKey(VolunteerOfferRequest, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    offer_status = models.CharField(max_length=20, choices=OfferStatus.choices, default=OfferStatus.OPEN)
