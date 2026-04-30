"""
apps/chatbot/router.py
-----------------------
Routeur intelligent qui choisit le meilleur modèle IA en fonction de :
  - la complexité de la question (intent + longueur de contexte)
  - la disponibilité des providers
  - le coût (modèles gratuits en priorité)
"""
import time
from typing import Optional

from apps.chatbot.intent_detector import IntentDetector


class IntelligentRouter:
    """
    Sélectionne le provider et le modèle optimal pour chaque question.
    Stratégie : modèle gratuit/rapide pour les questions simples,
    modèle puissant pour les analyses complexes.
    """

    # ── Configuration des modèles par tier ────────────────────────────────────
    TIERS = {
        'fast': {
            'label': 'Rapide (questions factuelles)',
            'providers': [
                {'name': 'gemini', 'model': 'gemini-2.0-flash'},
            ],
        },
        'balanced': {
            'label': 'Équilibré (analyses standard)',
            'providers': [
                {'name': 'mistral', 'model': 'mistral-small-latest'},
                {'name': 'gemini', 'model': 'gemini-2.0-flash'},
            ],
        },
        'powerful': {
            'label': 'Puissant (analyses complexes, diagnostics)',
            'providers': [
                {'name': 'mistral_rag', 'model': 'mistral-medium'},
                {'name': 'mistral', 'model': 'mistral-small-latest'},
                {'name': 'deepseek', 'model': 'deepseek/deepseek-r1:free'},
            ],
        },
    }

    # ── Mapping intention → tier ──────────────────────────────────────────────
    INTENT_TIER_MAP = {
        'general': 'balanced',
        'plantation': 'balanced',
        'diagnostic': 'powerful',
        'rendement': 'powerful',
        'meteo': 'fast',
        'sol': 'balanced',
        'marche': 'fast',
        'stockage': 'fast',
        'elevage': 'balanced',
    }

    def __init__(self):
        self._intent_detector = IntentDetector()
        self._provider_health = {}  # Track recent failures

    def route(self, question: str, context_size: int = 0,
              preferred_provider: str = None) -> dict:
        """
        Détermine le meilleur modèle pour la question donnée.

        Returns:
            {
                'tier': 'fast|balanced|powerful',
                'provider': 'gemini|mistral|mistral_rag|deepseek',
                'model': 'model-name',
                'intent': 'detected-intent',
                'language': 'fr|en|mg',
            }
        """
        analysis = self._intent_detector.analyze(question)
        intent = analysis['intent']
        language = analysis['language']

        # Déterminer le tier de base selon l'intention
        base_tier = self.INTENT_TIER_MAP.get(intent, 'balanced')

        # Ajuster si le contexte est volumineux
        if context_size > 2000:
            base_tier = 'powerful'
        elif context_size > 500 and base_tier == 'fast':
            base_tier = 'balanced'

        # Si une question longue ou complexe → monter en tier
        if len(question) > 200 or '?' in question and question.count('?') > 1:
            if base_tier == 'fast':
                base_tier = 'balanced'

        # Sélectionner le provider
        tier_config = self.TIERS[base_tier]
        providers = tier_config['providers']

        # Si le provider préféré est spécifié et disponible, l'utiliser
        if preferred_provider:
            for p in providers:
                if p['name'] == preferred_provider:
                    return {
                        'tier': base_tier,
                        'provider': p['name'],
                        'model': p['model'],
                        'intent': intent,
                        'language': language,
                        'confidence': analysis['confidence'],
                        'prompt_key': analysis['prompt_key'],
                    }

        # Sinon, choisir le premier provider "healthy"
        selected = providers[0]
        for p in providers:
            if self._is_healthy(p['name']):
                selected = p
                break

        return {
            'tier': base_tier,
            'provider': selected['name'],
            'model': selected['model'],
            'intent': intent,
            'language': language,
            'confidence': analysis['confidence'],
            'prompt_key': analysis['prompt_key'],
        }

    def mark_failure(self, provider_name: str):
        """Marque un provider comme défaillant temporairement."""
        self._provider_health[provider_name] = {
            'failed_at': time.time(),
            'cooldown_seconds': 120,
        }

    def mark_success(self, provider_name: str):
        """Restaure la santé d'un provider après un succès."""
        self._provider_health.pop(provider_name, None)

    def _is_healthy(self, provider_name: str) -> bool:
        """Vérifie si un provider est opérationnel."""
        health = self._provider_health.get(provider_name)
        if not health:
            return True
        elapsed = time.time() - health['failed_at']
        if elapsed > health['cooldown_seconds']:
            # Cooldown expiré, réessayer
            self._provider_health.pop(provider_name, None)
            return True
        return False

    def get_fallback_chain(self, primary_provider: str) -> list:
        """
        Retourne la chaîne de fallback quand le provider principal échoue.
        """
        all_providers = [
            {'name': 'gemini', 'model': 'gemini-2.0-flash'},
            {'name': 'mistral', 'model': 'mistral-small-latest'},
            {'name': 'deepseek', 'model': 'deepseek/deepseek-r1:free'},
            {'name': 'openrouter', 'model': 'meta-llama/llama-3.1-8b-instruct:free'},
        ]
        return [p for p in all_providers if p['name'] != primary_provider]
