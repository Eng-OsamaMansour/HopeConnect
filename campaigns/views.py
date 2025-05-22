from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from .models import Campaign
from .serializers import CampaignSerializer

# URL: /api/campaigns/
# Method: POST
# Only admin can create campaigns
class CampaignCreateView(generics.CreateAPIView):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    permission_classes = [IsAdminUser]

# URL: /api/campaigns/<id>/close/
# Method: PATCH
# Only admin can close campaigns
class CampaignCloseView(generics.UpdateAPIView):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    permission_classes = [IsAdminUser]

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
