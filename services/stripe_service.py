import stripe
from django.conf import settings
from typing import Dict, Any, Optional
from decimal import Decimal

class StripeService:
    def __init__(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        self.webhook_secret = settings.STRIPE_WEBHOOK_SECRET

    def create_payment_intent(
        self,
        amount: Decimal,
        currency: str,
        metadata: Dict[str, Any],
        payment_method_types: list = ['card']
    ) -> Dict[str, Any]:
        """
        Create a payment intent with Stripe
        """
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(float(amount) * 100),  # Convert to cents
                currency=currency.lower(),
                payment_method_types=payment_method_types,
                metadata=metadata
            )
            return {
                'id': intent.id,
                'client_secret': intent.client_secret,
                'status': intent.status
            }
        except stripe.error.StripeError as e:
            raise Exception(f"Stripe error: {str(e)}")

    def retrieve_payment_intent(self, payment_intent_id: str) -> Dict[str, Any]:
        """
        Retrieve a payment intent from Stripe
        """
        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            return {
                'id': intent.id,
                'status': intent.status,
                'amount': intent.amount / 100,  # Convert from cents
                'currency': intent.currency,
                'client_secret': intent.client_secret
            }
        except stripe.error.StripeError as e:
            raise Exception(f"Stripe error: {str(e)}")

    def confirm_payment_intent(
        self,
        payment_intent_id: str,
        payment_method: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Confirm a payment intent
        """
        try:
            intent = stripe.PaymentIntent.confirm(
                payment_intent_id,
                payment_method=payment_method
            )
            return {
                'id': intent.id,
                'status': intent.status,
                'client_secret': intent.client_secret
            }
        except stripe.error.StripeError as e:
            raise Exception(f"Stripe error: {str(e)}")

    def cancel_payment_intent(self, payment_intent_id: str) -> Dict[str, Any]:
        """
        Cancel a payment intent
        """
        try:
            intent = stripe.PaymentIntent.cancel(payment_intent_id)
            return {
                'id': intent.id,
                'status': intent.status
            }
        except stripe.error.StripeError as e:
            raise Exception(f"Stripe error: {str(e)}")

    def create_refund(
        self,
        payment_intent_id: str,
        amount: Optional[Decimal] = None
    ) -> Dict[str, Any]:
        """
        Create a refund for a payment
        """
        try:
            refund_params = {
                'payment_intent': payment_intent_id
            }
            if amount:
                refund_params['amount'] = int(float(amount) * 100)

            refund = stripe.Refund.create(**refund_params)
            return {
                'id': refund.id,
                'status': refund.status,
                'amount': refund.amount / 100
            }
        except stripe.error.StripeError as e:
            raise Exception(f"Stripe error: {str(e)}")

    def construct_webhook_event(self, payload: bytes, sig_header: str) -> stripe.Event:
        """
        Construct and verify a webhook event
        """
        try:
            event = stripe.Webhook.construct_event(
                payload,
                sig_header,
                self.webhook_secret
            )
            return event
        except stripe.error.SignatureVerificationError as e:
            raise Exception(f"Invalid signature: {str(e)}")
        except Exception as e:
            raise Exception(f"Webhook error: {str(e)}")

    def handle_payment_intent_succeeded(self, event: stripe.Event) -> Dict[str, Any]:
        """
        Handle successful payment intent
        """
        payment_intent = event.data.object
        return {
            'payment_intent_id': payment_intent.id,
            'status': 'COMPLETED',
            'amount': payment_intent.amount / 100,
            'currency': payment_intent.currency
        }

    def handle_payment_intent_failed(self, event: stripe.Event) -> Dict[str, Any]:
        """
        Handle failed payment intent
        """
        payment_intent = event.data.object
        return {
            'payment_intent_id': payment_intent.id,
            'status': 'FAILED',
            'error_message': payment_intent.last_payment_error.message if payment_intent.last_payment_error else 'Payment failed'
        }
