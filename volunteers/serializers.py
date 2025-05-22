from rest_framework import serializers
from .models import VolunteerOfferRequest, Volunteer

class VolunteerSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Volunteer
        fields = "__all__"

class VolunteerOfferRequestSerializer(serializers.ModelSerializer):
    volunteer = VolunteerSerializer(read_only=True)

    class Meta:
        model  = VolunteerOfferRequest
        fields = "__all__"
        read_only_fields = ("id", "status", "volunteer")
