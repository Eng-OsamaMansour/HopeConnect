from rest_framework import serializers
from .models import Payment
from donations.models import MoneyDonation

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id', 'donation', 'amount', 'currency', 'status',
            'payment_method', 'payment_intent_id', 'client_secret',
            'error_message', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'status', 'payment_intent_id', 'client_secret',
            'error_message', 'created_at', 'updated_at'
        ]

class CreatePaymentSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField(max_length=3, default="USD")
    payment_method = serializers.CharField(max_length=50)
    donation_id = serializers.IntegerField()

    def validate(self, data):
        try:
            donation = MoneyDonation.objects.get(id=data['donation_id'])
            if donation.amount != data['amount']:
                raise serializers.ValidationError("Amount doesn't match donation amount")
            if donation.currency != data['currency']:
                raise serializers.ValidationError("Currency doesn't match donation currency")
        except MoneyDonation.DoesNotExist:
            raise serializers.ValidationError("Donation not found")
        return data

class PaymentWebhookSerializer(serializers.Serializer):
    payment_intent_id = serializers.CharField()
    status = serializers.CharField()
    error_message = serializers.CharField(required=False, allow_blank=True)
