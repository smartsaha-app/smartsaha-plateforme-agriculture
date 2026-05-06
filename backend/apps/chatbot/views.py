"""
apps/chatbot/views.py
---------------------
v2.0 — Vues enrichies avec :
  - SmartAssistantViewSet : orchestrateur intelligent (mémoire + RAG + router)
  - Sessions de chat persistantes
  - Feedback utilisateur (👍/👎)
  - Conservation de tous les endpoints legacy existants

ViewSets disponibles :
    SmartAssistantViewSet     — ★ NOUVEAU : endpoint intelligent  → /api/v2/smart-assistant/
    AgriAssistantViewSet      — OpenRouter multi-modèles          → /api/v2/assistant/
    GeminiAssistantViewSet    — Google Gemini                     → /api/v2/gemini-assistant/
    MistralAssistantViewSet   — Mistral AI (public)               → /api/v2/mistral-assistant/

APIViews :
    AgronomyAssistantAPIView  — Mistral RAG + contexte parcel     → /api/v2/agronomy/
    ChatSessionListView       — Liste des sessions de chat         → /api/v2/chat/sessions/
    ChatSessionDetailView     — Détail d'une session               → /api/v2/chat/sessions/<uuid>/
    ChatFeedbackView          — Feedback sur un message            → /api/v2/chat/feedback/
    assistant_agronome_page   — page HTML                          → /assistant-agronome/
    assistant_agronome_api    — endpoint JSON CSRF-exempt           → /api/assistant-agronome/
"""
import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from apps.chatbot.services import (
    SimpleAIClient,
    RobustGeminiClient,
    MistralAgentClient,
    MistralRAGClient,
    SmartAssistant,
)
from apps.chatbot.models import ChatSession, ChatMessage, ChatFeedback

# ──────────────────────────────────────────────────────────────────────────────
# Instances partagées — instanciées à la demande (lazy)
# ──────────────────────────────────────────────────────────────────────────────
_mistral_rag_client = None
_smart_assistant = None


def _get_mistral_rag():
    global _mistral_rag_client
    if _mistral_rag_client is None:
        _mistral_rag_client = MistralRAGClient()
    return _mistral_rag_client


def _get_smart_assistant():
    global _smart_assistant
    if _smart_assistant is None:
        _smart_assistant = SmartAssistant()
    return _smart_assistant


# ══════════════════════════════════════════════════════════════════════════════
# ★ SmartAssistantViewSet — Endpoint intelligent principal (NOUVEAU)
# ══════════════════════════════════════════════════════════════════════════════
class SmartAssistantViewSet(viewsets.ViewSet):
    """
    Endpoint intelligent avec :
    - Mémoire conversationnelle (sessions persistantes)
    - Détection automatique de langue (FR/EN/MG)
    - Routage intelligent multi-modèles
    - Contexte RAG enrichi (parcelle + KB FOFIFA/FAOSTAT + alertes)
    - Feedback utilisateur
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Poser une question intelligente (Smart Assistant)",
        tags=['Assistant IA v2'],
        request=OpenApiTypes.OBJECT,
        responses={200: OpenApiTypes.OBJECT}
    )
    def create(self, request):
        """POST /api/v2/smart-assistant/ — Question avec IA intelligente"""
        question = request.data.get('question', '').strip()
        if not question:
            return Response(
                {'error': 'Le champ "question" est requis'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        session_id = request.data.get('session_id')
        parcel_id = request.data.get('parcel_id')
        crop_name = request.data.get('crop_name')
        user_modules = request.data.get('user_modules', {})

        try:
            # 1. Récupérer ou créer la session de chat
            session = self._get_or_create_session(request.user, session_id, parcel_id)

            # 2. Sauvegarder le message utilisateur
            user_msg = ChatMessage.objects.create(
                session=session,
                role='user',
                content=question,
            )

            # 3. Récupérer l'historique de conversation
            chat_history = session.get_history(last_n=8)

            # 4. Appeler le SmartAssistant
            assistant = _get_smart_assistant()
            result = assistant.ask(
                question=question,
                parcel_uuid=parcel_id,
                user_modules=user_modules,
                chat_history=chat_history,
                crop_name=crop_name,
                user=request.user,
            )

            # 5. Sauvegarder la réponse
            assistant_msg = ChatMessage.objects.create(
                session=session,
                role='assistant',
                content=result['answer'],
                metadata={
                    'provider': result['provider'],
                    'model': result['model'],
                    'intent': result['intent'],
                    'language': result['language'],
                    'response_time_ms': result['response_time_ms'],
                    'confidence': result['confidence'],
                    'context_used': result['context_used'],
                },
            )

            # 6. Auto-générer le titre de session si premier message
            session.auto_title()

            # 7. Mettre à jour la langue de session
            if session.language != result['language']:
                session.language = result['language']
                session.save(update_fields=['language'])

            return Response({
                'answer': result['answer'],
                'session_id': str(session.uuid),
                'message_id': assistant_msg.pk,
                'meta': {
                    'intent': result['intent'],
                    'language': result['language'],
                    'provider': result['provider'],
                    'model': result['model'],
                    'response_time_ms': result['response_time_ms'],
                    'confidence': result['confidence'],
                    'context_used': result['context_used'],
                    'session_title': session.title,
                },
                'timestamp': timezone.now().isoformat(),
            })

        except Exception as e:
            return Response(
                {'error': f'Erreur du service IA: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @extend_schema(
        summary="Informations sur le Smart Assistant",
        tags=['Assistant IA v2'],
        responses={200: OpenApiTypes.OBJECT}
    )
    def list(self, request):
        """GET /api/v2/smart-assistant/ — Informations sur le service"""
        return Response({
            'service': 'SmartSaha Assistant Agronome Intelligent',
            'version': '2.0',
            'features': [
                'Mémoire conversationnelle (sessions persistantes)',
                'Détection automatique de langue (FR/EN/MG)',
                'Routage intelligent multi-modèles',
                'Contexte RAG enrichi (parcelle + FOFIFA + FAOSTAT)',
                'Détection d\'intention (plantation, diagnostic, rendement...)',
                'Feedback utilisateur (👍/👎)',
            ],
            'supported_languages': ['fr', 'en', 'mg'],
            'endpoints': {
                'POST /': 'Poser une question',
                'GET /': 'Informations sur le service',
                'GET /sessions/': 'Lister les sessions de chat',
            },
            'timestamp': timezone.now().isoformat(),
        })

    @extend_schema(
        summary="Lister les sessions de chat",
        tags=['Assistant IA v2'],
        operation_id="smart_assistant_list_sessions",
        responses={200: OpenApiTypes.OBJECT}
    )
    @action(detail=False, methods=['get'])
    def sessions(self, request):
        """GET /api/v2/smart-assistant/sessions/ — Liste des sessions"""
        sessions = ChatSession.objects.filter(
            user=request.user, is_active=True
        ).order_by('-updated_at')[:20]

        return Response({
            'sessions': [
                {
                    'id': str(s.uuid),
                    'title': s.title or 'Sans titre',
                    'language': s.language,
                    'parcel_id': str(s.parcel_id) if s.parcel_id else None,
                    'messages_count': s.messages.count(),
                    'created_at': s.created_at.isoformat(),
                    'updated_at': s.updated_at.isoformat(),
                }
                for s in sessions
            ]
        })

    @extend_schema(
        summary="Historique d'une session de chat",
        tags=['Assistant IA v2'],
        operation_id="smart_assistant_get_session",
        parameters=[
            OpenApiParameter(name='session_uuid', type=OpenApiTypes.UUID, location=OpenApiParameter.PATH)
        ],
        responses={200: OpenApiTypes.OBJECT}
    )
    @action(detail=False, methods=['get'], url_path='sessions/(?P<session_uuid>[^/.]+)')
    def session_detail(self, request, session_uuid=None):
        """GET /api/v2/smart-assistant/sessions/<uuid>/ — Détail session"""
        try:
            session = ChatSession.objects.get(
                uuid=session_uuid, user=request.user
            )
        except ChatSession.DoesNotExist:
            return Response(
                {'error': 'Session introuvable'},
                status=status.HTTP_404_NOT_FOUND,
            )

        messages = session.messages.order_by('created_at')

        return Response({
            'session': {
                'id': str(session.uuid),
                'title': session.title,
                'language': session.language,
                'parcel_id': str(session.parcel_id) if session.parcel_id else None,
                'created_at': session.created_at.isoformat(),
            },
            'messages': [
                {
                    'id': msg.pk,
                    'role': msg.role,
                    'content': msg.content,
                    'metadata': msg.metadata,
                    'feedback': self._get_feedback(msg),
                    'created_at': msg.created_at.isoformat(),
                }
                for msg in messages
            ],
        })

    @extend_schema(
        summary="Supprimer une session de chat",
        tags=['Assistant IA v2'],
        parameters=[
            OpenApiParameter(name='session_uuid', type=OpenApiTypes.UUID, location=OpenApiParameter.PATH)
        ],
        responses={204: None}
    )
    @action(detail=False, methods=['delete'], url_path='sessions/(?P<session_uuid>[^/.]+)/delete')
    def delete_session(self, request, session_uuid=None):
        """DELETE /api/v2/smart-assistant/sessions/<uuid>/delete/ — Supprimer session"""
        try:
            session = ChatSession.objects.get(
                uuid=session_uuid, user=request.user
            )
            session.is_active = False
            session.save(update_fields=['is_active'])
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ChatSession.DoesNotExist:
            return Response(
                {'error': 'Session introuvable'},
                status=status.HTTP_404_NOT_FOUND,
            )

    @extend_schema(
        summary="Donner un feedback sur une réponse",
        tags=['Assistant IA v2'],
        request=OpenApiTypes.OBJECT,
        responses={200: OpenApiTypes.OBJECT}
    )
    @action(detail=False, methods=['post'])
    def feedback(self, request):
        """POST /api/v2/smart-assistant/feedback/ — Feedback sur une réponse"""
        message_id = request.data.get('message_id')
        rating = request.data.get('rating')
        comment = request.data.get('comment', '')

        if not message_id or rating not in (1, 2):
            return Response(
                {'error': 'message_id et rating (1 ou 2) sont requis'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            message = ChatMessage.objects.get(
                pk=message_id,
                role='assistant',
                session__user=request.user,
            )
        except ChatMessage.DoesNotExist:
            return Response(
                {'error': 'Message introuvable'},
                status=status.HTTP_404_NOT_FOUND,
            )

        feedback, created = ChatFeedback.objects.update_or_create(
            message=message,
            defaults={'rating': rating, 'comment': comment},
        )

        return Response({
            'success': True,
            'feedback_id': feedback.pk,
            'rating': '👍' if rating == 2 else '👎',
            'created': created,
        })

    # ── Méthodes utilitaires ─────────────────────────────────────────────────

    @staticmethod
    def _get_or_create_session(user, session_id=None, parcel_id=None):
        """Récupère une session existante ou en crée une nouvelle."""
        if session_id:
            try:
                session = ChatSession.objects.get(uuid=session_id, user=user, is_active=True)
                session.save(update_fields=['updated_at'])  # Touch
                return session
            except ChatSession.DoesNotExist:
                pass

        # Créer une nouvelle session
        kwargs = {'user': user}
        if parcel_id:
            from apps.parcels.models import Parcel
            try:
                kwargs['parcel'] = Parcel.objects.get(uuid=parcel_id)
            except Parcel.DoesNotExist:
                pass

        return ChatSession.objects.create(**kwargs)

    @staticmethod
    def _get_feedback(message):
        """Récupère le feedback d'un message si existant."""
        if message.role != 'assistant':
            return None
        try:
            fb = message.feedback
            return {'rating': fb.rating, 'comment': fb.comment}
        except ChatFeedback.DoesNotExist:
            return None


# ══════════════════════════════════════════════════════════════════════════════
# 1. AgriAssistantViewSet — OpenRouter (SimpleAIClient) — LEGACY
# ══════════════════════════════════════════════════════════════════════════════
@extend_schema(tags=['Assistant IA'])
class AgriAssistantViewSet(viewsets.ViewSet):
    """
    ViewSet complet pour l'assistant agronome (OpenRouter).
    Le client IA est instancié à la première requête, pas au démarrage.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._ai_client = None

    @property
    def ai_client(self):
        if self._ai_client is None:
            self._ai_client = SimpleAIClient()
        return self._ai_client

    @extend_schema(
        summary="Poser une question (OpenRouter)",
        tags=['Assistant IA'],
        request=OpenApiTypes.OBJECT,
        responses={200: OpenApiTypes.OBJECT}
    )
    def create(self, request):
        """POST /api/v2/assistant/ — Pose une question"""
        question = request.data.get('question', '').strip()
        if not question:
            return Response(
                {'error': 'Le champ "question" est requis'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        max_tokens = request.data.get('max_tokens', 1000)
        temperature = request.data.get('temperature', 0.7)

        try:
            reponse = self.ai_client.ask(question)
            return Response({
                'id': f"chat_{int(timezone.now().timestamp())}",
                'question': question,
                'reponse': reponse,
                'timestamp': timezone.now().isoformat(),
                'metadata': {'max_tokens': max_tokens, 'temperature': temperature},
            })
        except Exception as e:
            return Response(
                {'error': f'Erreur du service IA: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @extend_schema(
        summary="Informations sur le service (OpenRouter)",
        tags=['Assistant IA'],
        responses={200: OpenApiTypes.OBJECT}
    )
    def list(self, request):
        """GET /api/v2/assistant/ — Informations sur le service"""
        return Response({
            'service': 'Assistant Agronome Expert Madagascar',
            'version': '2.0',
            'description': 'Service IA pour conseils agricoles adaptés à Madagascar',
            'endpoints': {
                'POST /': 'Poser une question',
                'GET /status/': 'Statut du service',
                'POST /batch_ask/': 'Questions multiples (max 5)',
            },
            'timestamp': timezone.now().isoformat(),
        })

    @extend_schema(
        summary="Statut du service OpenRouter",
        tags=['Assistant IA'],
        responses={200: OpenApiTypes.OBJECT}
    )
    @action(detail=False, methods=['get'])
    def status(self, request):
        """GET /api/v2/assistant/status/"""
        return Response({
            'status': 'operational',
            'timestamp': timezone.now().isoformat(),
            'models_available': len(self.ai_client.models),
        })

    @extend_schema(
        summary="Questions multiples (OpenRouter)",
        tags=['Assistant IA'],
        request=OpenApiTypes.OBJECT,
        responses={200: OpenApiTypes.OBJECT}
    )
    @action(detail=False, methods=['post'])
    def batch_ask(self, request):
        """POST /api/v2/assistant/batch_ask/ — Questions multiples"""
        questions = request.data.get('questions', [])

        if not isinstance(questions, list) or len(questions) == 0:
            return Response(
                {'error': 'Le champ "questions" doit être une liste non vide'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if len(questions) > 5:
            return Response(
                {'error': 'Maximum 5 questions par requête'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        reponses = []
        for question in questions:
            if isinstance(question, str) and question.strip():
                try:
                    reponse = self.ai_client.ask(question.strip())
                    reponses.append({'question': question, 'reponse': reponse, 'status': 'success'})
                except Exception as e:
                    reponses.append({'question': question, 'reponse': None, 'status': 'error', 'error': str(e)})

        return Response({
            'batch_id': f"batch_{int(timezone.now().timestamp())}",
            'results': reponses,
            'timestamp': timezone.now().isoformat(),
        })


# ══════════════════════════════════════════════════════════════════════════════
# 2. GeminiAssistantViewSet — Google Gemini (RobustGeminiClient) — LEGACY
# ══════════════════════════════════════════════════════════════════════════════
@extend_schema(tags=['Assistant IA'])
class GeminiAssistantViewSet(viewsets.ViewSet):
    """ViewSet pour l'assistant agronome avec Gemini."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._ai_client = None

    @property
    def ai_client(self):
        if self._ai_client is None:
            self._ai_client = RobustGeminiClient()
        return self._ai_client

    @extend_schema(
        summary="Poser une question (Gemini)",
        tags=['Assistant IA'],
        request=OpenApiTypes.OBJECT,
        responses={200: OpenApiTypes.OBJECT}
    )
    def create(self, request):
        """POST /api/v2/gemini-assistant/"""
        question = request.data.get('question', '').strip()
        if not question:
            return Response(
                {'error': 'Le champ "question" est requis'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            reponse = self.ai_client.ask(question)
            return Response({
                'success': True,
                'question': question,
                'reponse': reponse,
                'timestamp': timezone.now().isoformat(),
            })
        except Exception as e:
            return Response(
                {'error': f'Erreur du service: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @extend_schema(
        summary="Informations sur le service (Gemini)",
        tags=['Assistant IA'],
        responses={200: OpenApiTypes.OBJECT}
    )
    def list(self, request):
        """GET /api/v2/gemini-assistant/"""
        return Response({
            'service': 'Assistant Agronome Gemini',
            'provider': 'Google Gemini',
            'model': 'gemini-2.0-flash',
            'timestamp': timezone.now().isoformat(),
        })


# ══════════════════════════════════════════════════════════════════════════════
# 3. MistralAssistantViewSet — Mistral AI (public) — LEGACY
# ══════════════════════════════════════════════════════════════════════════════
@extend_schema(tags=['Assistant IA'])
class MistralAssistantViewSet(viewsets.ViewSet):
    """ViewSet public pour Mistral — aucune authentification requise."""
    permission_classes = [AllowAny]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            self._agent_client = MistralAgentClient()
            self._error_message = None
        except Exception as e:
            self._agent_client = None
            self._error_message = f'Client non disponible: {str(e)}'

    @extend_schema(
        summary="Poser une question (Mistral Public)",
        tags=['Assistant IA'],
        request=OpenApiTypes.OBJECT,
        responses={200: OpenApiTypes.OBJECT}
    )
    def create(self, request):
        """POST /api/v2/mistral-assistant/"""
        question = request.data.get('question', '').strip()
        if not question:
            return Response(
                {'error': 'Le champ "question" est requis'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not self._agent_client:
            return Response({
                'success': False,
                'question': question,
                'reponse': self._error_message or 'Service temporairement indisponible',
                'fallback': True,
                'timestamp': timezone.now().isoformat(),
            })

        try:
            reponse = self._agent_client.ask(question)
            return Response({
                'success': True,
                'question': question,
                'reponse': reponse,
                'timestamp': timezone.now().isoformat(),
            })
        except Exception as e:
            return Response({
                'success': False,
                'question': question,
                'reponse': self._get_fallback_response(question),
                'error': str(e),
                'fallback': True,
                'timestamp': timezone.now().isoformat(),
            })

    @extend_schema(
        summary="Informations sur le service (Mistral)",
        tags=['Assistant IA'],
        responses={200: OpenApiTypes.OBJECT}
    )
    def list(self, request):
        """GET /api/v2/mistral-assistant/"""
        available = self._agent_client and self._agent_client.mistral_available
        return Response({
            'service': 'Assistant Agronome Mistral',
            'provider': 'Mistral AI',
            'status': 'actif' if available else 'inactif',
            'authentication': 'aucune requise',
            'usage': 'POST avec {"question": "votre question"}',
            'timestamp': timezone.now().isoformat(),
        })

    @staticmethod
    def _get_fallback_response(question: str) -> str:
        """Réponses de fallback quand l'API ne répond pas."""
        fallbacks = {
            'riz': 'À Madagascar, plantez le riz en novembre-décembre. Rendement moyen: 2-4 tonnes/ha.',
            'maïs': 'Maïs: plantation octobre-novembre. Cycle 90-120 jours. Rendement: 1.5-3 tonnes/ha.',
            'manioc': 'Manioc: tolérant aux sols pauvres. Rendement: 10-20 tonnes/ha.',
            'haricot': 'Haricot: fixe l\'azote. Bonne rotation avec céréales.',
            'pomme de terre': 'Pomme de terre: altitude >1000m. Plantation août-septembre. Rendement: 15-25 t/ha.',
        }
        q_lower = question.lower()
        for key, response in fallbacks.items():
            if key in q_lower:
                return f'Mode basique - {response}'
        return f'Service IA temporairement indisponible. Question reçue: {question[:100]}'


# ══════════════════════════════════════════════════════════════════════════════
# 4. AgronomyAssistantAPIView — Mistral RAG avec contexte parcel — LEGACY
# ══════════════════════════════════════════════════════════════════════════════
@extend_schema(tags=['Assistant IA'])
class AgronomyAssistantAPIView(APIView):
    """
    POST /api/agronomy/
    Appel Mistral RAG avec contexte parcel + modules utilisateur.
    Authentification via session cookie (héritée de settings.py).
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Assistant Agronome RAG (Mistral avec contexte)",
        tags=['Assistant IA'],
        request=OpenApiTypes.OBJECT,
        responses={200: OpenApiTypes.OBJECT}
    )
    def post(self, request):
        try:
            question = request.data.get('question')
            if not question:
                return Response(
                    {'error': 'Aucune question fournie.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            question_type = request.data.get('question_type', 'general')
            parcel_id = request.data.get('parcel_id')
            crop_name = request.data.get('crop_name')
            user_modules = request.data.get('user_modules', {})

            # Tentative avec Mistral RAG avec fallback vers Gemini
            rag_client = _get_mistral_rag()

            if not getattr(rag_client, 'mistral_available', False):
                from apps.chatbot.services import RobustGeminiClient
                print("Basculement preventif vers Gemini (Mistral indisponible)")
                answer = RobustGeminiClient().ask(question)
                provider = "Gemini (Fallback)"
            else:
                try:
                    answer = rag_client.ask(
                        question=question,
                        parcel_uuid=parcel_id,
                        user_modules=user_modules,
                        knowledge_query=question,
                        crop_name=crop_name,
                    )
                    provider = "Mistral"
                    if "Erreur API Mistral" in answer:
                         raise Exception("Mistral RAG Error")
                except Exception as e:
                    print(f"Erreur Mistral RAG: {e}. Basculement vers Gemini.")
                    from apps.chatbot.services import RobustGeminiClient
                    answer = RobustGeminiClient().ask(question)
                    provider = "Gemini (Fallback)"

            return Response({
                'answer': answer,
                'meta': {
                    'question_type': question_type,
                    'parcel_id': parcel_id,
                    'crop_name': crop_name,
                    'modules': user_modules,
                    'provider': provider
                },
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': f'Erreur interne: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# ══════════════════════════════════════════════════════════════════════════════
# 5. Vues HTML / JSON legacy — conservées pour rétrocompatibilité
# ══════════════════════════════════════════════════════════════════════════════
def assistant_agronome_page(request):
    """GET /assistant-agronome/ — Page HTML assistant."""
    return render(request, 'assistant_agronome.html')


@csrf_exempt
def assistant_agronome_api(request):
    """POST /api/assistant-agronome/ — Endpoint JSON CSRF-exempt (legacy)."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Payload JSON invalide'}, status=400)

    question = payload.get('question')
    question_type = payload.get('question_type')
    parcel_id = payload.get('parcel_id')
    crop_name = payload.get('crop_name')
    user_modules = payload.get('user_modules', {})

    if not question or not question_type:
        return JsonResponse({'error': 'Champs obligatoires manquants'}, status=400)

    response = _get_mistral_rag().ask(
        question=question,
        parcel_uuid=parcel_id,
        user_modules=user_modules,
    )
    return JsonResponse(response, safe=False)
