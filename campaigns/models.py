from django.db import models

class CampaignCategory(models.TextChoices):
    GENERAL    = "general",    "General"
    EMERGENCY  = "emergency",  "Emergency"

class Campaign(models.Model):
    title        = models.CharField(max_length=120)
    category     = models.CharField(max_length=20, choices=CampaignCategory.choices)
    goal_amount  = models.DecimalField(max_digits=10, decimal_places=2)
    start        = models.DateField()
    end          = models.DateField(null=True, blank=True)
    is_open      = models.BooleanField(default=True)         
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-start"]

    def __str__(self):
        return self.title