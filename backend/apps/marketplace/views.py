from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.marketplace.models import Post, PostImage, Cart, CartItem, Order, Review
from apps.marketplace.serializers import (
    PostSerializer, CartSerializer, CartItemSerializer, 
    OrderSerializer, ReviewSerializer
)

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'location', 'post_type']
    ordering_fields = ['created_at', 'price']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        from django.db.models import Q
        qs = Post.objects.all().prefetch_related('images').order_by('-created_at')
        
        # Pour les actions de modification : accès restreint au propriétaire
        if self.action in ['update', 'partial_update', 'destroy']:
            return qs.filter(author=self.request.user)

        # Pour le listing et le détail public
        if self.request.user.is_authenticated:
            # L'utilisateur voit ses produits (actifs/inactifs) et les produits actifs des autres
            return qs.filter(Q(author=self.request.user) | Q(is_active=True))
        
        # Utilisateur anonyme : uniquement les produits actifs
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
        post_uuid = request.data.get('post_uuid')
        quantity = request.data.get('quantity', 1)
        
        try:
            post = Post.objects.get(uuid=post_uuid)
        except Post.DoesNotExist:
            return Response({'error': 'Post non trouvé'}, status=status.HTTP_404_NOT_FOUND)

        item, created = CartItem.objects.get_or_create(cart=cart, post=post, defaults={'quantity': 0})
        item.quantity += float(quantity)
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

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Order.objects.all().order_by('-created_at')
        if not self.request.user.is_authenticated:
            return qs.none()
            
        as_seller = self.request.query_params.get('as_seller')
        as_buyer = self.request.query_params.get('as_buyer')
        
        if as_seller == 'true':
            return qs.filter(seller=self.request.user)
        if as_buyer == 'true':
            return qs.filter(buyer=self.request.user)
            
        # Par défaut, tout ce qui concerne l'utilisateur
        return qs.filter(buyer=self.request.user) | qs.filter(seller=self.request.user)

    def perform_create(self, serializer):
        post = serializer.validated_data['post']
        serializer.save(
            buyer=self.request.user,
            seller=post.author,
            total_price=post.price * serializer.validated_data['quantity']
        )

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(reviewer=self.request.user)

    def perform_create(self, serializer):
        order = serializer.validated_data['order']
        # L'utilisateur courant doit être l'acheteur de la commande
        if order.buyer != self.request.user:
            raise serializers.ValidationError("Seul l'acheteur peut laisser un avis.")
        
        serializer.save(
            reviewer=self.request.user,
            reviewee=order.seller
        )
