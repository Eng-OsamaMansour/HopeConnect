from django.db import models
from accounts.models import User
from orphanages.models import Orphanage


class OrphanGender(models.TextChoices):
    MALE   = "M", "Male"
    FEMALE = "F", "Female"

class Orphan(models.Model):
    orphanage = models.ForeignKey(Orphanage, on_delete=models.CASCADE, related_name="orphans")
    national_id = models.CharField(max_length=14, unique=True)
    name = models.CharField(max_length=120) 
    gender = models.CharField(max_length=1, choices=OrphanGender.choices)
    birth_date = models.DateField(null=True, blank=True)
    health_info = models.TextField(blank=True)
    education_status= models.CharField(max_length=255, blank=True)
    photo = models.ImageField(upload_to="orphans/%Y/%m", null=True, blank=True)

    def age(self):
        from datetime import date
        return date.today().year - self.birth_date.year if self.birth_date else None

    def __str__(self):
        return f"{self.name} ({self.orphanage})"

class OrphanSponsor(models.Model):
    orphan = models.ForeignKey(Orphan, on_delete=models.CASCADE, related_name="sponsors")
    donor = models.ForeignKey(User, on_delete=models.PROTECT, related_name="sponsorships", limit_choices_to={"role": "DONOR"})
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ("orphan", "donor")

class OrphanUpdate(models.Model):
    orphan = models.ForeignKey("Orphan", on_delete=models.CASCADE, related_name="updates")
    title = models.CharField(max_length=120)
    photo = models.ImageField(upload_to="orphan_updates/", blank=True, null=True)
    note = models.TextField(blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)