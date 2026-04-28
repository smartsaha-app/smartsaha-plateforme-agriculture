"""
apps/chatbot/intent_detector.py
--------------------------------
Détection d'intention pour adapter le prompt, le routing et le contexte.
Supporte le français, l'anglais et le malagasy.
"""
import re
from typing import Tuple, Optional


class IntentDetector:
    """
    Détecte l'intention de l'utilisateur et la langue utilisée
    pour adapter la réponse de l'assistant IA.
    """

    # ── Intentions et mots-clés multilingues ─────────────────────────────────
    INTENTS = {
        'plantation': {
            'keywords': [
                # FR
                'planter', 'semer', 'cultiver', 'plantation', 'semis', 'repiquage',
                'quand planter', 'date de semis', 'saison', 'pépinière',
                # EN
                'plant', 'sow', 'grow', 'when to plant', 'planting date', 'season',
                'nursery', 'seedbed',
                # MG
                'mamboly', 'fambolena', 'fotoana fambolena', 'mamafy',
                'tetiandro', 'fotoana famafy',
            ],
            'prompt_key': 'plantation',
        },
        'diagnostic': {
            'keywords': [
                # FR
                'maladie', 'malade', 'insecte', 'ravageur', 'problème', 'attaque',
                'feuilles jaunes', 'taches', 'pourrit', 'meurt', 'sèche',
                'chenille', 'puceron',
                # EN
                'disease', 'pest', 'problem', 'insect', 'yellow leaves', 'wilting',
                'dying', 'spots', 'caterpillar', 'aphid',
                # MG
                'aretina', 'marary', 'bibikely', 'olitra', 'mavo ny ravina',
                'simba', 'maty',
            ],
            'prompt_key': 'diagnostic',
        },
        'rendement': {
            'keywords': [
                # FR
                'rendement', 'récolte', 'production', 'combien', 'estimation',
                'tonne', 'kg/ha', 'productivité', 'résultat',
                # EN
                'yield', 'harvest', 'production', 'how much', 'estimate',
                'productivity', 'output',
                # MG
                'vokatra', 'fijinjana', 'firy', 'tarehimarika',
            ],
            'prompt_key': 'rendement',
        },
        'meteo': {
            'keywords': [
                # FR
                'pluie', 'temps', 'météo', 'sécheresse', 'cyclone', 'vent',
                'température', 'climat', 'inondation',
                # EN
                'rain', 'weather', 'drought', 'cyclone', 'wind', 'temperature',
                'climate', 'flood',
                # MG
                'orana', 'toetrandro', 'hain-tany', 'rivotra', 'tondra-drano',
                'hafanana',
            ],
            'prompt_key': 'meteo',
        },
        'sol': {
            'keywords': [
                # FR
                'sol', 'terre', 'engrais', 'compost', 'fertilisant', 'fumier',
                'pH', 'azote', 'phosphore', 'potassium', 'amendement',
                # EN
                'soil', 'fertilizer', 'compost', 'manure', 'nitrogen',
                'phosphorus', 'amendment',
                # MG
                'tany', 'zezika', 'fanampin-tany',
            ],
            'prompt_key': 'sol',
        },
        'marche': {
            'keywords': [
                # FR
                'prix', 'vendre', 'marché', 'acheteur', 'coût', 'bénéfice',
                'rentabilité', 'commerce',
                # EN
                'price', 'sell', 'market', 'buyer', 'cost', 'profit',
                'profitability',
                # MG
                'vidiny', 'mivarotra', 'tsena', 'mpividy', 'tombony',
            ],
            'prompt_key': 'marche',
        },
        'stockage': {
            'keywords': [
                # FR
                'stockage', 'conserver', 'conservation', 'sécher', 'séchage',
                'stocker', 'grenier', 'silo', 'post-récolte',
                # EN
                'storage', 'store', 'drying', 'preserve', 'post-harvest',
                'silo', 'granary',
                # MG
                'fitehirizana', 'manaikitra', 'manaina',
            ],
            'prompt_key': 'stockage',
        },
        'elevage': {
            'keywords': [
                # FR
                'boeuf', 'zébu', 'poulet', 'mouton', 'élevage', 'bétail',
                'volaille', 'porc',
                # EN
                'cattle', 'chicken', 'sheep', 'livestock', 'poultry', 'pig',
                # MG
                'omby', 'akoho', 'ondry', 'fiompiana', 'kisoa',
            ],
            'prompt_key': 'general',
        },
    }

    # ── Détection de langue ──────────────────────────────────────────────────
    LANGUAGE_MARKERS = {
        'mg': [
            'mba', 'ahoana', 'inona', 'fotoana', 'tokony', 'tsara',
            'manao ahoana', 'azafady', 'misaotra', 'mamboly', 'voly',
            'vary', 'katsaka', 'mangahazo', 'voanjo', 'tsaramaso',
            'tany', 'orana', 'ririnina', 'asara', 'tanety', 'tanimbary',
            'ny', 'ny tany', 'sy', 'ary', 'dia', 'izany', 'ho', 'aho',
        ],
        'en': [
            'what', 'when', 'how', 'where', 'which', 'should', 'could',
            'would', 'please', 'tell me', 'explain', 'the', 'is', 'are',
            'can', 'help', 'need', 'want', 'about', 'plant', 'crop',
            'farm', 'yield', 'soil', 'weather',
        ],
        'fr': [
            'comment', 'quand', 'pourquoi', 'quel', 'quelle', 'est-ce',
            'je', 'nous', 'vous', 'mon', 'mes', 'notre', 'votre',
            'le', 'la', 'les', 'du', 'des', 'un', 'une',
            'merci', 'bonjour', 's\'il vous plaît',
        ],
    }

    def detect_intent(self, question: str) -> Tuple[str, float]:
        """
        Détecte l'intention principale de la question.
        Retourne (intent_key, confidence_score).
        """
        q_lower = question.lower()
        scores = {}

        for intent_key, intent_data in self.INTENTS.items():
            score = 0
            for keyword in intent_data['keywords']:
                if keyword in q_lower:
                    # Bonus pour les mots-clés plus longs (plus spécifiques)
                    score += len(keyword.split())
            scores[intent_key] = score

        if not scores or max(scores.values()) == 0:
            return ('general', 0.0)

        best_intent = max(scores, key=scores.get)
        max_score = scores[best_intent]
        # Normaliser la confiance (max ~5 keywords matchés = 1.0)
        confidence = min(max_score / 5.0, 1.0)

        return (best_intent, confidence)

    def detect_language(self, text: str) -> str:
        """
        Détecte la langue du texte : 'fr', 'en', ou 'mg'.
        L'IA répondra dans cette langue.
        """
        t_lower = text.lower()
        words = set(re.findall(r'\b\w+\b', t_lower))

        scores = {}
        for lang, markers in self.LANGUAGE_MARKERS.items():
            score = sum(1 for marker in markers if marker in t_lower)
            # Bonus pour les marqueurs multi-mots
            for marker in markers:
                if ' ' in marker and marker in t_lower:
                    score += 2
            scores[lang] = score

        if not scores or max(scores.values()) == 0:
            return 'fr'  # Défaut français

        return max(scores, key=scores.get)

    def get_prompt_key(self, question: str) -> str:
        """Retourne la clé du prompt spécialisé à utiliser."""
        intent, confidence = self.detect_intent(question)
        if confidence < 0.2:
            return 'general'
        return self.INTENTS.get(intent, {}).get('prompt_key', 'general')

    def analyze(self, question: str) -> dict:
        """
        Analyse complète d'une question :
        retourne intention, langue, et prompt_key.
        """
        intent, confidence = self.detect_intent(question)
        language = self.detect_language(question)
        prompt_key = self.get_prompt_key(question)

        return {
            'intent': intent,
            'confidence': round(confidence, 2),
            'language': language,
            'prompt_key': prompt_key,
        }
