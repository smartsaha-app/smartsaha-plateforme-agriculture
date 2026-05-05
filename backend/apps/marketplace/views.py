from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.marketplace.models import Category, Product, Cart, CartItem, Order, OrderItem, Review
from apps.marketplace.serializers import (
    CategorySerializer, ProductSerializer, CartSerializer, 
    CartItemSerializer, OrderSerializer, ReviewSerializer
)
from django.db import transaction
from rest_framework.parsers import MultiPartParser, FormParser
import uuid

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all().order_by('order', 'name')
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'category__name', 'source_type']
    ordering_fields = ['created_at', 'price']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

    def get_queryset(self):
        from django.db.models import Q
        qs = Product.objects.all().order_by('-created_at')
        
        if self.action in ['update', 'partial_update', 'destroy']:
            return qs.filter(seller=self.request.user)

        if self.request.user.is_authenticated:
            return qs.filter(Q(seller=self.request.user) | Q(is_active=True))
        
        return qs.filter(is_active=True)

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

    @action(detail=False, methods=['post'])
    def add_item(self, request):
        cart = self.get_object()
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Produit non trouvé'}, status=status.HTTP_404_NOT_FOUND)

        item, created = CartItem.objects.get_or_create(
            cart=cart, 
            product=product, 
            defaults={'quantity': 0, 'price': product.price}
        )
        item.quantity += quantity
        if not created:
            item.price = product.price # Mettre à jour le snapshot du prix
        item.save()
        
        return Response(CartSerializer(cart).data)

    @action(detail=False, methods=['post'])
    def remove_item(self, request):
        cart = self.get_object()
        item_id = request.data.get('item_id')
        try:
            item = CartItem.objects.get(id=item_id, cart=cart)
            item.delete()
        except CartItem.DoesNotExist:
            return Response({'error': 'Item non trouvé'}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(CartSerializer(cart).data)

    @action(detail=False, methods=['post'])
    @transaction.atomic
    def checkout(self, request):
        cart = self.get_object()
        items = cart.items.all()
        
        if not items.exists():
            return Response({'error': 'Le panier est vide'}, status=status.HTTP_400_BAD_REQUEST)

        delivery_fee = request.data.get('delivery_fee', 0)
        subtotal = sum(item.subtotal for item in items)
        total = float(subtotal) + float(delivery_fee)
        
        import datetime
        order_num = f"CMD-{datetime.date.today().year}-{str(uuid.uuid4())[:8].upper()}"

        order = Order.objects.create(
            order_number=order_num,
            buyer=request.user,
            buyer_name=request.data.get('buyer_name', request.user.get_full_name() or request.user.username),
            subtotal=subtotal,
            delivery_fee=delivery_fee,
            total=total,
            payment_method=request.data.get('payment_method', 'MVOLA'),
            delivery_name=request.data.get('delivery_name', ''),
            delivery_phone=request.data.get('delivery_phone', ''),
            delivery_address=request.data.get('delivery_address', ''),
            delivery_city=request.data.get('delivery_city', ''),
            delivery_region=request.data.get('delivery_region', ''),
            delivery_notes=request.data.get('delivery_notes', ''),
        )
        
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                seller=item.product.seller,
                seller_name=item.product.seller.username if item.product.seller else 'Inconnu',
                product_name=item.product.name,
                product_image=item.product.image_url,
                quantity=item.quantity,
                price=item.price,
                subtotal=item.subtotal
            )

        # Vider le panier
        items.delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        # Si as_seller=true, on retourne les commandes contenant des produits de ce vendeur
        if self.request.query_params.get('as_seller') == 'true':
            return Order.objects.filter(items__seller=user).distinct().order_by('-created_at')
            
        # Par défaut, on voit ses propres achats
        return Order.objects.filter(buyer=user).order_by('-created_at')

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(reviewer=self.request.user)

    def perform_create(self, serializer):
        order_item = serializer.validated_data['order_item']
        if order_item.order.buyer != self.request.user:
            raise serializers.ValidationError("Vous ne pouvez noter que les produits que vous avez achetés.")
        
        serializer.save(
            reviewer=self.request.user,
            reviewee=order_item.seller
        )
