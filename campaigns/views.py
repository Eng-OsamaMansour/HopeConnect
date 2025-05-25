from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from accounts.permissions import IsAdmin
from rest_framework.response import Response
from .models import Campaign
from donations.models import Donation
from .serializers import CampaignSerializer
from donations.serializers import DonationSerializer

# URL: /api/campaigns/
# Method: POST
# Only admin can create campaigns
class CampaignCreateView(generics.CreateAPIView):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    permission_classes = [IsAdmin]

# URL: /api/campaigns/<id>/close/
# Method: PATCH
# Only admin can close campaigns
class CampaignCloseView(generics.UpdateAPIView):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    permission_classes = [IsAdmin]

    def patch(self, request, *args, **kwargs):
        campaign = self.get_object()
        campaign.is_open = False
        campaign.save()
        serializer = self.get_serializer(campaign)
        return Response(serializer.data)

# URL: /api/campaigns/open/
# Method: GET
# Anyone can view open campaigns
class OpenCampaignsListView(generics.ListAPIView):
    serializer_class = CampaignSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Campaign.objects.filter(is_open=True)


# URL: /api/campaigns/<id>/donations/
# Method: GET
# Admin can view donations for a campaign
class CampaignDonationsListView(generics.ListAPIView):
    serializer_class = DonationSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        campaign = Campaign.objects.get(id = self.kwargs['pk'])
        return Donation.objects.filter(campaign=campaign)
