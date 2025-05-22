from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Payment
from .serializers import (
    PaymentSerializer,
    CreatePaymentSerializer,
    PaymentWebhookSerializer
)
from donations.models import MoneyDonation
from services.stripe_service import StripeService
from django.http import HttpResponse
import json

class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    stripe_service = StripeService()

    def get_queryset(self):
        return Payment.objects.filter(donation__donor=self.request.user)

    @action(detail=False, methods=['post'])
    def create_payment_intent(self, request):
        serializer = CreatePaymentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        donation = get_object_or_404(MoneyDonation, id=data['donation_id'])

        try:
            # Create payment intent using StripeService
            intent_data = self.stripe_service.create_payment_intent(
                amount=data['amount'],
                currency=data['currency'],
                metadata={
                    'donation_id': donation.id,
                    'user_id': request.user.id
                }
            )

            # Create payment record
            payment = Payment.objects.create(
                donation=donation,
                amount=data['amount'],
                currency=data['currency'],
                payment_method=data['payment_method'],
                payment_intent_id=intent_data['id'],
                client_secret=intent_data['client_secret']
            )

            return Response({
                'client_secret': intent_data['client_secret'],
                'payment_id': payment.id
            })

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['post'])
    def webhook(self, request):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

        try:
            # Verify and construct the webhook event
            event = self.stripe_service.construct_webhook_event(payload, sig_header)

            # Handle the event
            if event.type == 'payment_intent.succeeded':
                payment_data = self.stripe_service.handle_payment_intent_succeeded(event)
            elif event.type == 'payment_intent.payment_failed':
                payment_data = self.stripe_service.handle_payment_intent_failed(event)
            else:
                return HttpResponse(status=200)

            # Update payment record
            payment = get_object_or_404(
                Payment,
                payment_intent_id=payment_data['payment_intent_id']
            )
            payment.status = payment_data['status']
            if 'error_message' in payment_data:
                payment.error_message = payment_data['error_message']
            payment.save()

            # Update donation status if payment is completed
            if payment_data['status'] == 'COMPLETED':
                payment.donation.status = 'COMPLETED'
                payment.donation.save()

            return HttpResponse(status=200)

        except Exception as e:
            return HttpResponse(str(e), status=400)

    @action(detail=True, methods=['post'])
    def refund(self, request, pk=None):
        payment = self.get_object()
        
        try:
            refund_data = self.stripe_service.create_refund(
                payment_intent_id=payment.payment_intent_id
            )
            
            payment.status = 'REFUNDED'
            payment.save()
            
            return Response({
                'status': 'success',
                'refund_id': refund_data['id'],
                'amount': refund_data['amount']
            })
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
