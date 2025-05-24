from django.db import models
from accounts.models import User
from matcher.embeddings import embed_text
from orphanages.models import Orphanage
import json

class Volunteer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,limit_choices_to={"role": "VOLUNTEER"})
    skills = models.JSONField( blank=True)  
    availability = models.JSONField( blank=True)  
    def __str__(self):
        return str(self.user)

class OfferStatus(models.TextChoices):
    OPEN     = "OPEN",     "Open"
    MATCHED  = "MATCHED",  "Matched"
    DONE     = "DONE",     "Done"


class VolunteerOfferRequest(models.Model):
    volunteer = models.ForeignKey("volunteers.Volunteer", on_delete=models.CASCADE, related_name="offer_requests")
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('OPEN', 'Open'), ('MATCHED', 'Matched')], default='OPEN')
    embedding = models.TextField(null=True, blank=True)
    is_open = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        text = f"{self.title}. {self.description}"
        embedding_list = embed_text(text).tolist()  # Should return 1D list
        self.embedding = json.dumps(embedding_list)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title[:30]}... ({self.status})"

