from rest_framework import serializers
from orphan.serializers import OrphanSerializer
from .models import Orphanage, OrphanageNeedRequest, Review


class OrphanageSerializer(serializers.ModelSerializer):
    avg_rating   = serializers.FloatField(read_only=True)
    rating_count = serializers.IntegerField(read_only=True)
    orphans      = OrphanSerializer(many=True, read_only=True)
    class Meta:
        model  = Orphanage
        fields = "__all__"
        read_only_fields = ("id",)


class ReviewSerializer(serializers.ModelSerializer):
    donor_email = serializers.CharField(source="donor.email", read_only=True)
    class Meta:
        model  = Review
        fields = ("id", "stars", "comment", "donor_email", "created_at", "orphanage")
        read_only_fields = ("id", "donor_email", "created_at", "orphanage")


class OrphanageNeedRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model  = OrphanageNeedRequest
        fields = ("id","title","description","created_at","is_open",)
        read_only_fields = ("id","embedding","orphanage")
        

