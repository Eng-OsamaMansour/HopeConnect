import stripe
from django.conf import settings
from decimal import Decimal
from donations.models import Donation

stripe.api_key = settings.STRIPE_API_KEY

class StripeService:
    @staticmethod
    def create_payment_intent(amount: Decimal, *, currency=None, metadata=None) -> stripe.PaymentIntent:
        """
        amount = major units (e.g., 50.00 USD) – will convert to cents.
        """
        currency = currency or settings.STRIPE_CURRENCY
        intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),            # to cents
            currency=currency.lower(),
            automatic_payment_methods={"enabled": True},
            metadata=metadata or {},
        )
        return intent
    
    @staticmethod
    def retrieve_intent(intent_id: str) -> stripe.PaymentIntent:
        return stripe.PaymentIntent.retrieve(intent_id)

    def create_payment_intent(donation: Donation):
        fee = (donation.amount * settings.DONATION_FEE_PCT).quantize(Decimal("0.01"))
        intent = stripe.PaymentIntent.create(
            amount=int(donation.amount * 100),     # cents
            currency=donation.currency,
            automatic_payment_methods={"enabled": True},
            application_fee_amount=int(fee * 100),  # ← fee is taken automatically
            transfer_data={"destination": settings.FEE_RECEIVER_STRIPE_ACC},
            metadata={"donation_id": str(donation.id)},
        )
        donation.platform_fee = fee
        donation.save(update_fields=["platform_fee"])
        return intent.client_secret
