from rest_framework import viewsets, permissions, filters
from apps.catalogue.models import Category, Product
from apps.catalogue.serializers import CategorySerializer, ProductSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema, extend_schema_view

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all().order_by('order', 'name')
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

@extend_schema_view(
    list=extend_schema(tags=['Catalogue (Produits)']),
    retrieve=extend_schema(tags=['Catalogue (Produits)']),
    create=extend_schema(tags=['Catalogue (Produits)']),
    update=extend_schema(tags=['Catalogue (Produits)']),
    partial_update=extend_schema(tags=['Catalogue (Produits)']),
    destroy=extend_schema(tags=['Catalogue (Produits)']),
)
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
        if getattr(self, 'swagger_fake_view', False):
            return Product.objects.none()

        from django.db.models import Q
        qs = Product.objects.all().order_by('-created_at')
        
        # Modification/suppression : uniquement ses propres produits
        if self.action in ['update', 'partial_update', 'destroy']:
            return qs.filter(seller=self.request.user)

        # Vendeur : voit ses propres produits (actifs ou non) + tous les produits actifs des autres
        if self.request.user.is_authenticated and hasattr(self.request.user, 'pk'):
            seller_param = self.request.query_params.get('seller')
            if seller_param == 'me':
                # Mode vendeur : uniquement les produits du vendeur connecté
                return qs.filter(seller=self.request.user)
            # Acheteur/utilisateur général : uniquement les produits actifs
            return qs.filter(is_active=True)
        
        return qs.filter(is_active=True)
