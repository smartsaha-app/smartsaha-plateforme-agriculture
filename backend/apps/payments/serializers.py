from rest_framework import serializers
from .models import Transaction, PaymentMethod, Escrow, Refund, Invoice, Dispute, Subscription


class SubscriptionUserSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    email = serializers.EmailField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    role = serializers.CharField()
    plan = serializers.CharField()
    plan_expires_at = serializers.DateTimeField(allow_null=True)


class SubscriptionSerializer(serializers.ModelSerializer):
    user = SubscriptionUserSerializer(read_only=True)

    class Meta:
        model = Subscription
        fields = ['id', 'user', 'plan', 'status', 'started_at', 'expires_at', 'payment_ref', 'provider']
        read_only_fields = ['id', 'started_at']


class SubscriptionUpgradeSerializer(serializers.Serializer):
    plan = serializers.ChoiceField(choices=['FREE', 'PRO'])
    duration_days = serializers.IntegerField(min_value=1, max_value=3650, default=30)
    payment_ref = serializers.CharField(max_length=100, required=False, allow_blank=True)
    provider = serializers.ChoiceField(
        choices=['STRIPE', 'MVOLA', 'ORANGE_MONEY', 'AIRTEL_MONEY', 'MANUAL'],
        required=False,
        allow_null=True,
    )


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
    order_id = serializers.IntegerField()
    method = serializers.ChoiceField(choices=PaymentMethod.PROVIDER_CHOICES)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    # Payment token is for Stripe or similar gateways
    payment_token = serializers.CharField(required=False, allow_blank=True)

class DisputeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispute
        fields = ['id', 'transaction', 'opened_by', 'reason', 'status', 'created_at', 'resolved_at', 'resolution_notes']
        read_only_fields = ['id', 'opened_by', 'status', 'created_at', 'resolved_at', 'resolution_notes']
