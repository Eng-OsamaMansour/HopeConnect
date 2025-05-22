from rest_framework import serializers
from .models import Delivery, Location

class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Delivery
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"
        read_only_fields = ("id")


