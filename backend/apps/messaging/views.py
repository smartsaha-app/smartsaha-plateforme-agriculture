from rest_framework import viewsets, permissions, status, decorators
from rest_framework.response import Response
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    """
    Gestion des conversations (Boîte de réception).
    """
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Un utilisateur ne voit que ses propres conversations
        return Conversation.objects.filter(participants=self.request.user)

    @swagger_auto_schema(tags=['Messaging'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Messaging'])
    def create(self, request, *args, **kwargs):
        """
        Initie une conversation. 
        Si une conversation existe déjà entre ces participants pour ce post, elle est retournée.
        """
        other_user_uuid = request.data.get('other_user_uuid')
        related_post_id = request.data.get('related_post')
        
        if not other_user_uuid:
            return Response({"error": "other_user_uuid est requis"}, status=status.HTTP_400_BAD_REQUEST)

        # Rechercher si une conversation existe déjà
        existing = Conversation.objects.filter(
            participants=request.user
        ).filter(
            participants__uuid=other_user_uuid,
            related_post_id=related_post_id
        ).first()

        if existing:
            return Response(ConversationSerializer(existing, context={'request': request}).data)

        # Création sinon
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation = serializer.save()
        conversation.participants.add(request.user, other_user_uuid)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MessageViewSet(viewsets.ModelViewSet):
    """
    Gestion des messages unitaires.
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        # L'expéditeur est toujours l'utilisateur connecté
        serializer.save(sender=self.request.user)
        # Mettre à jour la date de la conversation pour le tri
        serializer.instance.conversation.save()

    @swagger_auto_schema(tags=['Messaging'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Messaging'])
    @decorators.action(detail=False, methods=['post'], url_path='mark-as-read')
    def mark_as_read(self, request):
        """Marque tous les messages d'une conversation comme lus."""
        conversation_uuid = request.data.get('conversation')
        if not conversation_uuid:
            return Response({"error": "conversation UUID requis"}, status=status.HTTP_400_BAD_REQUEST)
        
        Message.objects.filter(
            conversation__uuid=conversation_uuid,
            is_read=False
        ).exclude(sender=request.user).update(is_read=True)
        
        return Response({"status": "messages marqués comme lus"})
