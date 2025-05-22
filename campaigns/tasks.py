from celery import shared_task
from django.core.mail import send_mass_mail
from django.conf import settings
from .models import Campaign, CampaignCategory
from accounts.models import User

@shared_task
def notify_new_emergency_campaign(campaign_id):
    try:
        campaign = Campaign.objects.get(id=campaign_id)
        if campaign.category != CampaignCategory.EMERGENCY:
            return "Not an emergency campaign"

        # Get all users' emails
        all_users = User.objects.all().values_list("email", flat=True)
        
        subject = f"Urgent: New Emergency Campaign - {campaign.title}"
        body = (
            f"Dear HopeConnect Community,\n\n"
            f"We want to bring your immediate attention to a new emergency campaign "
            f"that has just been launched on our platform.\n\n"
            f"Campaign Details:\n"
            f"Title: {campaign.title}\n"
            f"Goal: {campaign.goal_amount} {getattr(settings, 'STRIPE_CURRENCY', 'USD').upper()}\n"
            f"Start Date: {campaign.start}\n\n"
            f"This is an emergency campaign that requires urgent support from our community. "
            f"Your contribution can make a significant difference in this time of need.\n\n"
            f"To contribute to this cause, please visit your HopeConnect dashboard.\n\n"
            f"Thank you for your continued support and generosity.\n\n"
            f"Best regards,\nThe HopeConnect Team"
        )

        messages = [
            (subject, body, settings.DEFAULT_FROM_EMAIL, [email])
            for email in all_users
        ]
        
        send_mass_mail(messages, fail_silently=True)
        return f"Emergency campaign notification sent to {len(messages)} users"
    
    except Campaign.DoesNotExist:
        return "Campaign not found"

