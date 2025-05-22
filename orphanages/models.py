from django.db import models

from django.db import models
from accounts.models import User
from matcher.embeddings import embed_text



class Orphanage(models.Model):
    manager = models.OneToOneField(User, on_delete=models.PROTECT,limit_choices_to={"role": "ORPHANAGE"})
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=120)
    latitude  = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    verification_doc = models.FileField(upload_to="verification/", blank=True)
    is_public_approved = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class OrphanageNeedRequest(models.Model):
    orphanage = models.ForeignKey("Orphanage",on_delete=models.CASCADE,related_name="need_requests")
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    embedding = models.ArrayField(models.FloatField(), null=True, blank=True)
    is_open = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.orphanage} – {self.title}"
    def save(self, *args, **kwargs):
        text = f"{self.title}. {self.description}"
        self.embedding = embed_text(text).tolist()
        super().save(*args, **kwargs)


class Review(models.Model):
    orphanage = models.ForeignKey("Orphanage",on_delete=models.CASCADE,related_name="reviews")
    donor = models.ForeignKey("accounts.User",on_delete=models.CASCADE,limit_choices_to={"role": "DONOR"})
    stars = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ("orphanage", "donor")      
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.orphanage} – {self.stars}★ by {self.donor}"
        