from venv import logger
from celery import shared_task
from django.db.models import Q
from django.dispatch import receiver
from scipy.spatial.distance import cosine
from orphanages.models import OrphanageNeedRequest
from volunteers.models import VolunteerOfferRequest
from django.core.mail import send_mail
from django.conf import settings
from django.db.models.signals import post_save

from .models import (
    Matcher,
    OfferStatus
)
SIMILARITY_THRESHOLD = 0.75
@shared_task
def run_semantic_matching():
    needs  = OrphanageNeedRequest.objects.filter(is_open=True, embedding__isnull=False)
    offers = VolunteerOfferRequest.objects.filter(is_open=True, status=OfferStatus.OPEN, embedding__isnull=False)

    for need in needs:
        best_offer = None
        best_score = 1.0  
        for offer in offers:
            if Matcher.objects.filter(need_request=need, volunteer_offer=offer).exists():
                continue
            dist = cosine(need.embedding, offer.embedding)
            if dist < best_score:
                best_score = dist
                best_offer = offer

        if best_offer and (1 - best_score) >= SIMILARITY_THRESHOLD:
            Matcher.objects.create(
                need_request=need,
                volunteer_offer=best_offer
            )
            best_offer.status = OfferStatus.MATCHED
            best_offer.is_open = False
            best_offer.save(update_fields=["status", "is_open"])

            need.is_open = False
            need.save(update_fields=["is_open"])

@shared_task
def send_match_notification_emails(match_id):
    try:
        match = Matcher.objects.get(id=match_id)
        volunteer_email = match.volunteer_offer.volunteer.user.email
        volunteer_name = match.volunteer_offer.volunteer.user.get_full_name()
        orphanage_name = match.need_request.orphanage.name
        
        volunteer_subject = f"You've been matched with {orphanage_name}!"
        volunteer_message = f"""
        Dear {volunteer_name},
        
        Your offer has been matched with a need from {orphanage_name}.
        Please log in to view the details and next steps.
        
        Thank you for your support!
        """
        
        orphanage_email = match.need_request.orphanage.email
        orphanage_contact = match.need_request.orphanage.contact_person
        
        orphanage_subject = f"A volunteer has been matched to your need request"
        orphanage_message = f"""
        Dear {orphanage_contact},
        
        A volunteer has been matched to fulfill your need request.
        Please log in to view the volunteer's details and next steps.
        
        Thank you for using our platform!
        """
        
        send_mail(volunteer_subject, volunteer_message, settings.DEFAULT_FROM_EMAIL, [volunteer_email])
        send_mail(orphanage_subject, orphanage_message, settings.DEFAULT_FROM_EMAIL, [orphanage_email])
        
    except Matcher.DoesNotExist:
        logger.error(f"Match with ID {match_id} not found")
    except Exception as e:
        logger.error(f"Error sending match notification emails: {str(e)}")


@receiver(post_save, sender=OrphanageNeedRequest)
@receiver(post_save, sender=VolunteerOfferRequest)
def kick_matcher(sender, **kwargs):
    run_semantic_matching.delay()