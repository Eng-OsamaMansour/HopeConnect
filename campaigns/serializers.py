from rest_framework import serializers
from donations.models import Campaign


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Campaign
        fields = ("id", "title", "goal_amount", "start", "end", "is_open")