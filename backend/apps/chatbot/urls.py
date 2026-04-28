"""
apps/chatbot/urls.py
--------------------
Routes pour le module Assistant IA SmartSaha.

v2.0:
  ★ NOUVEAU :
    - /api/v2/smart-assistant/        — SmartAssistant intelligent (POST=question, GET=info)
    - /api/v2/smart-assistant/sessions/    — Lister les sessions
    - /api/v2/smart-assistant/sessions/<uuid>/ — Détail session
    - /api/v2/smart-assistant/feedback/    — Feedback 👍/👎

  LEGACY (conservés) :
    - /api/v2/assistant/              — OpenRouter
    - /api/v2/gemini-assistant/       — Google Gemini
    - /api/v2/mistral-assistant/      — Mistral AI (public)
    - /api/v2/agronomy/               — Mistral RAG
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.chatbot.views import (
    SmartAssistantViewSet,
    AgriAssistantViewSet,
    GeminiAssistantViewSet,
    MistralAssistantViewSet,
    AgronomyAssistantAPIView,
    assistant_agronome_page,
    assistant_agronome_api,
)

# ── Routeur API ───────────────────────────────────────────────────────────────
router = DefaultRouter()

# ★ NOUVEAU — Smart Assistant (endpoint principal recommandé)
router.register(r'smart-assistant', SmartAssistantViewSet, basename='smart-assistant')

# Legacy — endpoints existants conservés
router.register(r'assistant', AgriAssistantViewSet, basename='assistant')
router.register(r'gemini-assistant', GeminiAssistantViewSet, basename='gemini-assistant')
router.register(r'mistral-assistant', MistralAssistantViewSet, basename='mistral-assistant')


# ── URLs ──────────────────────────────────────────────────────────────────────
urlpatterns = [
    # API REST v2 — tous les viewsets
    path('v2/', include(router.urls)),

    # Agronomy RAG — endpoint direct (legacy)
    path('v2/agronomy/', AgronomyAssistantAPIView.as_view(), name='agronomy-assistant'),

    # Vues HTML / JSON legacy
    path('assistant-agronome/', assistant_agronome_page, name='assistant_agronome_page'),
    path('assistant-agronome/', assistant_agronome_api, name='assistant_agronome_api'),
]