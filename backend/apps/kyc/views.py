from rest_framework import viewsets, permissions, status, decorators
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import KYCDocument
from .serializers import KYCDocumentSerializer, KYCReviewSerializer

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
    queryset = KYCDocument.objects.all()
    serializer_class = KYCDocumentSerializer
    permission_classes = [permissions.IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]
    lookup_field = 'uuid'

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        tags=['KYC - Admin'],
        summary="Approuver ou rejeter un document KYC",
        request=KYCReviewSerializer,
        responses={200: KYCDocumentSerializer}
    )
    @decorators.action(detail=True, methods=['patch'])
    def review(self, request, pk=None):
        document = self.get_object()
        serializer = KYCReviewSerializer(document, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save(reviewed_by=request.user)
            
            # Si le document est approuvé, on peut mettre à jour le statut KYC de l'utilisateur
            if document.status == 'APPROVED':
                user = document.user
                user.kyc_status = 'APPROVED'
                user.save()
            
            return Response(KYCDocumentSerializer(document).data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
