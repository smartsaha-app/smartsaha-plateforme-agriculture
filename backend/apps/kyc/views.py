from rest_framework import viewsets, permissions, status, decorators
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import KYCDocument
from .serializers import KYCDocumentSerializer, KYCReviewSerializer


class KYCPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

@extend_schema_view(
    list=extend_schema(tags=['KYC']),
    retrieve=extend_schema(tags=['KYC']),
    create=extend_schema(tags=['KYC']),
    update=extend_schema(tags=['KYC']),
    partial_update=extend_schema(tags=['KYC']),
    destroy=extend_schema(tags=['KYC']),
)
class KYCViewSet(viewsets.ModelViewSet):
    """
    Vue pour les agriculteurs et organisations (Soumission KYC).
    """
    serializer_class = KYCDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    lookup_field = 'uuid'

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return KYCDocument.objects.none()
        return KYCDocument.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        # Remettre le statut KYC de l'utilisateur à PENDING lors d'un nouveau dépôt
        user = self.request.user
        if user.kyc_status != 'APPROVED':
            user.kyc_status = 'PENDING'
            user.save(update_fields=['kyc_status'])
        serializer.save(user=user)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

@extend_schema_view(
    list=extend_schema(tags=['KYC - Admin']),
    retrieve=extend_schema(tags=['KYC - Admin']),
)
class KYCAdminViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Vue pour les administrateurs (Revue KYC).
    """
    serializer_class = KYCDocumentSerializer
    permission_classes = [permissions.IsAdminUser]
    parser_classes = [JSONParser]
    lookup_field = 'uuid'
    pagination_class = KYCPagination

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return KYCDocument.objects.none()
        qs = KYCDocument.objects.select_related('user', 'reviewed_by').all()
        status_filter = self.request.query_params.get('status', '').upper()
        search = self.request.query_params.get('search', '').strip()
        if status_filter in ('PENDING', 'APPROVED', 'REJECTED'):
            qs = qs.filter(status=status_filter)
        if search:
            qs = qs.filter(
                user__email__icontains=search
            ) | qs.filter(
                user__first_name__icontains=search
            ) | qs.filter(
                user__last_name__icontains=search
            )
        return qs

    @extend_schema(tags=['KYC - Admin'], summary="Statistiques globales des documents KYC", responses={200: {}})
    @decorators.action(detail=False, methods=['get'])
    def stats(self, request):
        qs = KYCDocument.objects.all()
        return Response({
            'total':    qs.count(),
            'pending':  qs.filter(status='PENDING').count(),
            'approved': qs.filter(status='APPROVED').count(),
            'rejected': qs.filter(status='REJECTED').count(),
        })

    @extend_schema(
        tags=['KYC - Admin'],
        summary="Approuver ou rejeter un document KYC",
        request=KYCReviewSerializer,
        responses={200: KYCDocumentSerializer}
    )
    @decorators.action(detail=True, methods=['patch'])
    def review(self, request, uuid=None):
        document = self.get_object()
        serializer = KYCReviewSerializer(document, data=request.data, partial=True)
        
        if serializer.is_valid():
            updated_doc = serializer.save(reviewed_by=request.user)

            if updated_doc.status == 'APPROVED':
                user = updated_doc.user
                user.kyc_status = 'APPROVED'
                user.save()
            elif updated_doc.status == 'REJECTED':
                user = updated_doc.user
                user.kyc_status = 'REJECTED'
                user.save()

            return Response(KYCDocumentSerializer(updated_doc).data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
