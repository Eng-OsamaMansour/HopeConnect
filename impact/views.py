from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from accounts.permissions import IsDonor
from donations.models import Donation, OrphanSponsor
from logistics.models import Delivery
from orphanages.models import Orphan
from .serializers import (
    DonationBriefSerializer, SponsorBriefSerializer,
    DeliveryBriefSerializer, OrphanWithUpdatesSerializer,
)

class MyImpactView(APIView):
    permission_classes = [IsAuthenticated & IsDonor]

    @extend_schema(
        summary="Aggregated impact data for current donor",
        responses={200: dict},
    )
    def get(self, request):
        donor = request.user.donor

        donations   = DonationBriefSerializer(
            Donation.objects.filter(donor=donor).order_by("-created_at"), many=True
        ).data

        sponsorships = SponsorBriefSerializer(
            OrphanSponsor.objects.filter(donor=donor), many=True
        ).data

        deliveries  = DeliveryBriefSerializer(
            Delivery.objects.filter(donation__donor=donor), many=True
        ).data

        sponsored_orphans = Orphan.objects.filter(
            sponsors__donor=donor
        ).distinct()

        orphan_updates = OrphanWithUpdatesSerializer(
            sponsored_orphans, many=True
        ).data

        return Response({
            "donations": donations,
            "sponsorships": sponsorships,
            "deliveries": deliveries,
            "orphans": orphan_updates,
        })
