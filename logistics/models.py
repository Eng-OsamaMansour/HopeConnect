from django.db import models
from donations.models import Donation

class DeliveryStatus(models.TextChoices):
    PENDING = "pending"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    
class Location(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()


class Delivery(models.Model):
    donation = models.OneToOneField(Donation, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=DeliveryStatus.choices, default=DeliveryStatus.PENDING)
    pickup_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="pickup_deliveries",null=True, blank=True)
    dropOff_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="dropOff_deliveries",null=True, blank=True)
    current_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="current_deliveries",null=True, blank=True)
    pickup_date = models.DateField(null=True, blank=True)
    dropOff_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.donation.donor.name} - {self.donation.orphan.name}"
