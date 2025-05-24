from django.db import models
from accounts.models import User
from orphan.models import Orphan
from campaigns.models import Campaign


class DonationStatus(models.TextChoices):
    PENDING    = "PENDING",    "Pending"
    COMPLETED  = "COMPLETED",  "Completed"
    FAILED     = "FAILED",     "Failed"
    REFUNDED   = "REFUNDED",   "Refunded"


class DonationCategory(models.TextChoices):
    GENERAL   = "GENERAL",   "General"
    EDUCATION = "EDUCATION", "Education"
    MEDICAL   = "MEDICAL",   "Medical"
    MONEY = "MONEY","Money"

class DonationType(models.TextChoices):
    ORPHAN = "ORPHAN", "Orphan"
    CAMPAIGN = "CAMPAIGN", "Campaign"



class Donation(models.Model):
    donor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="donations",
        limit_choices_to={"role": "DONOR"}
    )
    orphan = models.ForeignKey(
        Orphan,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="donations"
    )    
    campaign = models.ForeignKey(
        Campaign,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="donations"
    )
    platform_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    donation_category = models.CharField(
        max_length=20,
        choices=DonationCategory.choices,
        default=DonationCategory.MONEY
    )
    status = models.CharField(
        max_length=20,
        choices=DonationStatus.choices,
        default=DonationStatus.PENDING
        )
    donation_type = models.CharField(
        max_length=20,
        choices=DonationType.choices,
        default=DonationType.ORPHAN
    )
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.donation_type.title()} Donation by {self.donor}"


class GeneralDonation(Donation):
    description = models.TextField(blank=True)
    material = models.CharField(max_length=255, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    need_transportation = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.donation_category = DonationCategory.GENERAL
        if self.orphan:
            self.campaign = None
            self.donation_type = DonationType.ORPHAN
        elif self.campaign:
            self.orphan = None
            self.donation_type = DonationType.CAMPAIGN
        super().save(*args, **kwargs)


class EducationDonation(Donation):
    field = models.CharField(max_length=255, blank=True)
    course = models.CharField(max_length=255, blank=True)
    course_duration = models.PositiveIntegerField(default=1)
    hours_per_week = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        self.donation_category = DonationCategory.EDUCATION
        super().save(*args, **kwargs)


class MedicalDonation(Donation):
    supply_type = models.CharField(max_length=255, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        self.donation_type = DonationCategory.MEDICAL
        self.donation_category = DonationCategory.MEDICAL
        super().save(*args, **kwargs)


class MoneyDonation(Donation):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    pay_for = models.CharField(max_length=255, blank=True)
    currency = models.CharField(max_length=3, default="USD")
    payment_intent_id = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        self.donation_type = DonationCategory.MONEY
        self.donation_category = DonationCategory.MONEY
        super().save(*args, **kwargs)

class DonationReport(models.Model):
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE, related_name="reports")
    report = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)




    



