from rest_framework import serializers
from .models import Transaction, PaymentMethod, Escrow, Refund, Invoice, Dispute

class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ['id', 'provider', 'phone', 'card_last4', 'is_default', 'created_at']
        read_only_fields = ['id', 'created_at']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'id', 'order', 'buyer', 'method', 'amount', 'currency', 
            'provider_transaction_id', 'phone', 'status', 'created_at', 'completed_at'
        ]
        read_only_fields = ['id', 'buyer', 'status', 'provider_transaction_id', 'created_at', 'completed_at']

class PaymentInitiateSerializer(serializers.Serializer):
    order_id = serializers.UUIDField()
    method = serializers.ChoiceField(choices=PaymentMethod.PROVIDER_CHOICES)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    # Payment token is for Stripe or similar gateways
    payment_token = serializers.CharField(required=False, allow_blank=True)

class DisputeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispute
        fields = ['id', 'transaction', 'opened_by', 'reason', 'status', 'created_at', 'resolved_at', 'resolution_notes']
        read_only_fields = ['id', 'opened_by', 'status', 'created_at', 'resolved_at', 'resolution_notes']
