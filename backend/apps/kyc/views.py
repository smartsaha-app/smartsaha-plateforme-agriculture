from rest_framework import viewsets, permissions, status, decorators
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .models import KYCDocument
from .serializers import KYCDocumentSerializer, KYCReviewSerializer

class KYCViewSet(viewsets.ModelViewSet):
    """
    Vue pour les agriculteurs et organisations (Soumission KYC).
    """
    serializer_class = KYCDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return KYCDocument.objects.filter(user=self.request.user)

    @swagger_auto_schema(tags=['KYC'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=['KYC'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class KYCAdminViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Vue pour les administrateurs (Revue KYC).
    """
    queryset = KYCDocument.objects.all()
    serializer_class = KYCDocumentSerializer
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(tags=['KYC - Admin'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=['KYC - Admin'],
        operation_summary="Approuver ou rejeter un document KYC",
        request_body=KYCReviewSerializer
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
