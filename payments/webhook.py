import stripe, json, logging
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from donations.models import Donation, DonationStatus
from donations.signals import donation_completed  # defined below

logger = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE_API_KEY

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig     = request.headers.get("Stripe-Signature", "")
    try:
        event = stripe.Webhook.construct_event(
            payload, sig, settings.STRIPE_WEBHOOK_SECRET
        )
    except (ValueError, stripe.error.SignatureVerificationError) as exc:
        logger.warning("Invalid Stripe webhook: %s", exc)
        return HttpResponseBadRequest()

    # Handle only succeeded intents
    if event["type"] == "payment_intent.succeeded":
        intent = event["data"]["object"]
        donation_id = intent["metadata"].get("donation_id")
        if donation_id:
            Donation.objects.filter(id=donation_id).update(status=DonationStatus.COMPLETED)
            donation_completed.send(sender="stripe", donation_id=donation_id)
    return HttpResponse(status=200)
