from rest_framework import serializers
from .models import KYCDocument

class KYCDocumentSerializer(serializers.ModelSerializer):
    """Serializer pour les utilisateurs (soumission de document)."""
    status_display   = serializers.CharField(source='get_status_display', read_only=True)
    doc_type_display = serializers.CharField(source='get_doc_type_display', read_only=True)
    user_email       = serializers.EmailField(source='user.email', read_only=True)
    user_first_name  = serializers.CharField(source='user.first_name', read_only=True)
    user_last_name   = serializers.CharField(source='user.last_name', read_only=True)

    class Meta:
        model = KYCDocument
        fields = [
            'uuid', 'doc_type', 'doc_type_display', 'file_url',
            'status', 'status_display', 'rejection_reason', 'created_at',
            'user_email', 'user_first_name', 'user_last_name',
        ]
        read_only_fields = ['uuid', 'status', 'rejection_reason', 'created_at',
                            'user_email', 'user_first_name', 'user_last_name']

    def create(self, validated_data):
        # L'utilisateur est automatiquement l'auteur du document
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class KYCReviewSerializer(serializers.ModelSerializer):
    """Serializer pour l'admin (revue de document)."""
    class Meta:
        model = KYCDocument
        fields = ['status', 'rejection_reason']

    def validate(self, data):
        # Si on rejette, une raison est obligatoire
        if data.get('status') == 'REJECTED' and not data.get('rejection_reason'):
            raise serializers.ValidationError({"rejection_reason": "Une raison est obligatoire en cas de rejet."})
        return data
