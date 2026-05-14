from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.orders.models import Cart, CartItem, Order, OrderItem, Review
from apps.catalogue.models import Product
from apps.orders.serializers import (
    CartSerializer, CartItemSerializer, OrderSerializer, ReviewSerializer
)
from django.db import transaction
import uuid
import datetime
from drf_spectacular.utils import extend_schema

@extend_schema(tags=['Marketplace (Panier)'])
class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Cart.objects.none()
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
        
        # Vérification des stocks
        new_quantity = item.quantity + quantity
        if new_quantity > product.stock:
            return Response(
                {'error': f'Désolé, seulement {product.stock} {product.unit} disponibles.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        item.quantity = new_quantity
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
        
        # Vérification des stocks avant de créer la commande
        for item in items:
            if item.product.stock < item.quantity:
                return Response(
                    {'error': f'Stock insuffisant pour {item.product.name} (Disponible: {item.product.stock})'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        total = float(subtotal) + float(delivery_fee)
        
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


@extend_schema(tags=['Marketplace (Commandes)'])
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Order.objects.none()
            
        user = self.request.user
        
        # Filtre de base : l'utilisateur est soit l'acheteur, soit le vendeur d'un article
        from django.db.models import Q
        queryset = Order.objects.filter(Q(buyer=user) | Q(items__seller=user)).distinct()
        
        # Filtre additionnel si on veut spécifiquement les ventes
        if self.request.query_params.get('as_seller') == 'true':
            queryset = queryset.filter(items__seller=user).distinct()
            
        return queryset.order_by('-created_at')

    @action(detail=True, methods=['post'], url_path='update-status')
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get('status')
        user = request.user

        # Vérification des permissions de base
        # Le vendeur peut confirmer et expédier
        # L'acheteur peut confirmer la réception (DELIVERED)
        is_seller = order.items.filter(seller=user).exists()
        is_buyer = (order.buyer == user)

        valid_statuses = [s[0] for s in Order.STATUS_CHOICES]
        if new_status not in valid_statuses:
            return Response({"error": "Statut invalide"}, status=status.HTTP_400_BAD_REQUEST)

        # Logique de transition
        if new_status == 'CONFIRMED' and not is_seller:
            return Response({"error": "Seul le vendeur peut confirmer la commande"}, status=status.HTTP_403_FORBIDDEN)
        
        if new_status == 'SHIPPED' and not is_seller:
            return Response({"error": "Seul le vendeur peut expédier la commande"}, status=status.HTTP_403_FORBIDDEN)

        if new_status == 'DELIVERED':
            if not (is_seller or is_buyer):
                return Response({"error": "Permission refusée"}, status=status.HTTP_403_FORBIDDEN)
            
            # Si livraison confirmée, on libère le séquestre
            from apps.payments.services import PaymentService
            PaymentService.release_escrow(order)

        order.status = new_status
        order.save()

        return Response(OrderSerializer(order).data)

@extend_schema(tags=['Marketplace (Avis)'])
class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Review.objects.none()
        return Review.objects.filter(reviewer=self.request.user)

    def perform_create(self, serializer):
        from rest_framework import serializers
        order_item = serializer.validated_data['order_item']
        if order_item.order.buyer != self.request.user:
            raise serializers.ValidationError("Vous ne pouvez noter que les produits que vous avez achetés.")
        
        serializer.save(
            reviewer=self.request.user,
            reviewee=order_item.seller
        )
