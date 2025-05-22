from rest_framework import serializers
from donations.models import Donation, OrphanSponsor
from logistics.models import Delivery
from orphanages.serializers import OrphanUpdateSerializer
from orphanages.models import Orphan

class DonationBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Donation
        fields = ['id', 'donor', 'orphan', 'campaign', 'donation_category', 'donation_type', 'status', 'created_at']


class DeliveryBriefSerializer(serializers.ModelSerializer):
    distance_km = serializers.SerializerMethodField()
    eta_minutes = serializers.SerializerMethodField()

    def get_distance_km(self, obj):
        return (obj.distance_m or 0) / 1000

    def get_eta_minutes(self, obj):
        return round((obj.duration_s or 0) / 60)

    class Meta:
        model  = Delivery
        fields = ("id", "status", "distance_km", "eta_minutes", "polyline")

class OrphanWithUpdatesSerializer(serializers.ModelSerializer):
    updates = OrphanUpdateSerializer(many=True, read_only=True)

    class Meta:
        model  = Orphan
        fields = ("id", "name", "gender", "birth_date", "updates")
