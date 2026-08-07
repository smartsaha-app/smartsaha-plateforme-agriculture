from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field, OpenApiTypes
from apps.orders.models import Cart, CartItem, Order, OrderItem, Review
from django.contrib.auth import get_user_model

User = get_user_model()

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_image = serializers.URLField(source='product.image_url', read_only=True)
    subtotal = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'product_name', 'product_image', 'quantity', 'price', 'subtotal', 'added_at']
        read_only_fields = ['cart', 'price', 'added_at']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    items_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total', 'items_count', 'created_at', 'updated_at']
        read_only_fields = ['user']

class OrderItemSerializer(serializers.ModelSerializer):
    product_image = serializers.URLField(source='product.image_url', read_only=True)
    product_stock = serializers.IntegerField(source='product.stock', read_only=True)
    subtotal = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'id', 'order', 'product', 'seller', 'seller_name', 
            'product_name', 'product_image', 'product_stock', 'quantity', 'price', 
            'subtotal', 'status'
        ]
        read_only_fields = ['id', 'order', 'product', 'seller', 'price', 'subtotal']

class OrderSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    buyer_details = serializers.SerializerMethodField()
    checkout_orders = serializers.SerializerMethodField()
    checkout_total = serializers.SerializerMethodField()
    subtotal = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    total = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'checkout_reference', 'checkout_orders', 'checkout_total',
            'buyer', 'buyer_details', 'buyer_name',
            'subtotal', 'delivery_fee', 'total', 'status', 'payment_method', 
            'payment_status', 'delivery_name', 'delivery_phone', 'delivery_address', 
            'delivery_city', 'delivery_region', 'delivery_notes', 'items', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'order_number', 'buyer', 'buyer_details', 'subtotal', 'total', 'created_at', 'updated_at']

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_buyer_details(self, obj):
        if not obj.buyer:
            return None
        return {
            'username': obj.buyer.username,
            'email': obj.buyer.email
        }

    def get_items(self, obj):
        items = obj.items.all()
        request = self.context.get('request')
        if request and request.user != obj.buyer:
            items = items.filter(seller=request.user)
        return OrderItemSerializer(items, many=True, context=self.context).data

    def get_checkout_orders(self, obj):
        request = self.context.get('request')
        if not obj.checkout_reference or not request or request.user != obj.buyer:
            return []
        orders = obj.__class__.objects.filter(
            buyer=obj.buyer,
            checkout_reference=obj.checkout_reference,
        ).order_by('created_at')
        return [
            {
                'id': order.id,
                'order_number': order.order_number,
                'subtotal': order.subtotal,
                'delivery_fee': order.delivery_fee,
                'total': order.total,
                'status': order.status,
                'payment_status': order.payment_status,
            }
            for order in orders
        ]

    def get_checkout_total(self, obj):
        if not obj.checkout_reference:
            return obj.total
        return sum(
            (order.total for order in obj.__class__.objects.filter(
                buyer=obj.buyer,
                checkout_reference=obj.checkout_reference,
            )),
            start=0,
        )

class ReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.CharField(source='reviewer.get_full_name', read_only=True)
    product_name = serializers.CharField(source='order_item.product_name', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'order_item', 'product_name', 'reviewer', 'reviewer_name', 'reviewee', 'rating', 'comment', 'created_at']
        read_only_fields = ['reviewer', 'reviewee', 'created_at']
