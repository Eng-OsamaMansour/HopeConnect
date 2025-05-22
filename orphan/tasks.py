from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import OrphanUpdate
from donations.models import Sponsorship

@shared_task
def notify_sponsor_of_orphan_update(update_id):
    try:
        update = OrphanUpdate.objects.get(id=update_id)
        orphan = update.orphan
        
        # Get active sponsorships for this orphan
        sponsorships = Sponsorship.objects.filter(
            orphan=orphan,
            is_active=True
        ).select_related('donor')
        
        for sponsorship in sponsorships:
            subject = f"New Update About {orphan.name}"
            message = (
                f"Dear {sponsorship.donor.get_full_name()},\n\n"
                f"We have a new update about {orphan.name} that we'd like to share with you.\n\n"
                f"Update Date: {update.created_at.strftime('%B %d, %Y')}\n"
                f"Update Details:\n{update.note}\n\n"
                f"Thank you for your continued support in making a difference "
                f"in {orphan.name}'s life.\n\n"
                f"Best regards,\nThe HopeConnect Team"
            )
            
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[sponsorship.donor.email],
                fail_silently=True
            )
        
        return f"Update notification sent to {sponsorships.count()} sponsor(s)"
        
    except OrphanUpdate.DoesNotExist:
        return "Orphan update not found"