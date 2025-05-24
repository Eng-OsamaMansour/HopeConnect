from celery import shared_task
from django.db.models.signals import post_save
from django.dispatch import receiver
from scipy.spatial.distance import cosine
from orphanages.models import OrphanageNeedRequest
from volunteers.models import VolunteerOfferRequest
from django.core.mail import send_mail
from django.conf import settings
import numpy as np
import os
import json

from .models import Matcher, OfferStatus

SIMILARITY_THRESHOLD = 0.75
IS_SEEDING = os.environ.get('DJANGO_SEEDING', 'False').lower() == 'true'


@shared_task
def run_semantic_matching():
    needs = OrphanageNeedRequest.objects.filter(is_open=True, embedding__isnull=False)
    offers = VolunteerOfferRequest.objects.filter(is_open=True, status=OfferStatus.OPEN, embedding__isnull=False)

    for need in needs:
        try:
            need_vec = parse_embedding(need.embedding)
        except Exception as e:
            print(f"❌ Error parsing need embedding: {e}")
            continue

        best_offer = None
        best_score = 1.0

        for offer in offers:
            if Matcher.objects.filter(need_request=need, volunteer_offer=offer).exists():
                continue
            try:
                offer_vec = parse_embedding(offer.embedding)
                dist = cosine(need_vec, offer_vec)
            except Exception as e:
                print(f"❌ Error parsing offer embedding: {e}")
                continue

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


def parse_embedding(raw):
    """
    Converts stored JSON string to 1D NumPy array.
    """
    arr = np.array(json.loads(raw))
    if arr.ndim > 1:
        arr = arr.flatten()
    if arr.ndim != 1:
        raise ValueError("Embedding must be 1-D after flattening.")
    return arr


@shared_task
def send_match_notification_email(match_id):
    if IS_SEEDING:
        return
    try:
        match = Matcher.objects.get(id=match_id)
        subject = 'New Match Found!'
        message = f"""
Dear {match.user.get_full_name()},

We have found a potential match for you!

Match Details:
- Type: {match.get_match_type_display()}
- Score: {match.score}
- Created: {match.created_at.strftime('%B %d, %Y')}

Please log in to your account to view the full details of this match.

Best regards,
The HopeConnect Support Team
        """
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [match.user.email],
            fail_silently=False,
        )
        print("📧 Match Notification Email Sent to:", match.user.email)
    except Matcher.DoesNotExist:
        pass


@receiver(post_save, sender=Matcher)
def match_post_save(sender, instance, created, **kwargs):
    if IS_SEEDING:
        return
    if created:
        send_match_notification_email.delay(instance.id)
