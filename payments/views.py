from rest_framework import generics, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from accounts.permissions import IsDonor, IsAdmin
from services.stripe_service import StripeService
from donations.models import Donation

class DonationPaymentIntentView(generics.GenericAPIView):
    """
    POST /api/donations/{id}/intent/  → returns client_secret
    """
    permission_classes = [IsDonor | IsAdmin]

    @extend_schema(responses={200: dict})
    def post(self, request, pk):
        donation = generics.get_object_or_404(Donation, pk=pk)
        if donation.payment_intent_id:
            intent = StripeService.retrieve_intent(donation.payment_intent_id)
        else:
            intent = StripeService.create_payment_intent(
                amount=donation.amount,
                metadata={"donation_id": donation.id},
            )
            donation.payment_intent_id = intent.id
            donation.save(update_fields=["payment_intent_id"])
        return Response({"client_secret": intent.client_secret}, status=status.HTTP_200_OK)
