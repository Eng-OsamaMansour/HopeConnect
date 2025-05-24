from rest_framework import serializers
from .models import (
    Donation, DonationReport, GeneralDonation, EducationDonation, 
    MedicalDonation, MoneyDonation
)


class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = [
            'id', 'donor', 'orphan', 'campaign', 'platform_fee',
            'donation_category', 'donation_type', 'status', 'created_at'
        ]
        read_only_fields = ['donor', 'status']


class GeneralDonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralDonation
        fields = [
            'id', 'donor', 'orphan', 'campaign', 'platform_fee',
            'donation_category', 'donation_type', 'status', 'created_at',
            'description', 'material', 'quantity', 'need_transportation'
        ]
        read_only_fields = ['donor', 'status', 'donation_category', 'donation_type']


class EducationDonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationDonation
        fields = [
            'id', 'donor', 'orphan', 'campaign', 'platform_fee',
            'donation_category', 'donation_type', 'status', 'created_at',
            'field', 'course', 'course_duration', 'hours_per_week'
        ]
        read_only_fields = ['donor', 'status', 'donation_category', 'donation_type']


class MedicalDonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalDonation
        fields = [
            'id', 'donor', 'orphan', 'campaign', 'platform_fee',
            'donation_category', 'donation_type', 'status', 'created_at',
            'supply_type', 'quantity', 'description'
        ]
        read_only_fields = ['donor', 'status', 'donation_category', 'donation_type']


class MoneyDonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoneyDonation
        fields = [
            'id', 'donor', 'orphan', 'campaign', 'platform_fee',
            'donation_category', 'donation_type', 'status', 'created_at',
            'amount', 'currency', 'payment_intent_id', 'pay_for'
        ]
        read_only_fields = ['donor', 'status', 'donation_category', 'donation_  type', 'payment_intent_id']


class DonationReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationReport
        fields = ['id', 'donation', 'report', 'created_at']
        read_only_fields = ['donation', 'created_at']
        


