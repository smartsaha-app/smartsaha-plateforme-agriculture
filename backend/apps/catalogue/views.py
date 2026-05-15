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
        user = self.request.user
        qs = Product.objects.all().order_by('-created_at')
        
        # Pour la modification/suppression : seul le propriétaire peut agir
        if self.action in ['update', 'partial_update', 'destroy']:
            if not user.is_authenticated:
                return qs.none()
            return qs.filter(seller=user)

        # Pour le détail (retrieve) : le proprio voit tout, les autres voient seulement si actif
        if self.action == 'retrieve':
            if user.is_authenticated:
                return qs.filter(Q(is_active=True) | Q(seller=user))
            return qs.filter(is_active=True)

        # Pour la liste (list)
        seller_param = self.request.query_params.get('seller')
        if seller_param == 'me' and user.is_authenticated:
            return qs.filter(seller=user)
        
        # Par défaut, on ne montre que les produits actifs
        return qs.filter(is_active=True)
