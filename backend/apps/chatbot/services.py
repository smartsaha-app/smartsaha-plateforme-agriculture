"""
apps/chatbot/services.py
------------------------
v2.0 — Services IA avec :
  - Prompts spécialisés par intention (plantation, diagnostic, rendement, etc.)
  - Support multilingue (FR, EN, MG)
  - Intégration du routeur intelligent
  - Historique conversationnel
  - Contexte RAG enrichi (parcelle + KB + FAOSTAT)

Classes disponibles :
    SimpleAIClient       — OpenRouter (deepseek, zephyr, openchat)
    RobustGeminiClient   — Google Gemini (HTTP direct, sans SDK)
    MistralAgentClient   — Mistral AI
    DeepSeekClient       — OpenRouter deepseek-r1 avec contexte parcel
    GeminiClient         — Google Gemini via SDK genai avec contexte parcel
    WorkingAIClient      — OpenRouter multi-modèles avec fallback automatique
    MistralRAGClient     — Mistral RAG avec contexte parcel
    SmartAssistant       — ★ NOUVEAU : orchestrateur intelligent (router + KB + mémoire)
"""
import os
import time
import httpx
import requests as http_requests

from django.conf import settings

from apps.chatbot.context_builder import ContextBuilder
from apps.chatbot.intent_detector import IntentDetector
from apps.chatbot.router import IntelligentRouter


# ══════════════════════════════════════════════════════════════════════════════
# Prompts multilingues spécialisés par intention
# ══════════════════════════════════════════════════════════════════════════════

LANGUAGE_INSTRUCTIONS = {
    'fr': "Réponds TOUJOURS en français.",
    'en': "ALWAYS respond in English.",
    'mg': "Valio amin'ny teny Malagasy foana. Respond ALWAYS in Malagasy language.",
}

SYSTEM_PROMPTS = {
    'general': {
        'fr': """Tu es Dr. Andry Rakoto, ingénieur agronome expert à Madagascar, employé par SmartSaha.
Tu conseilles les agriculteurs malgaches au quotidien.

RÈGLES :
- Réponds de manière précise, pratique et adaptée aux conditions locales de Madagascar
- Utilise des listes à puces pour les étapes
- Cite tes sources quand tu utilises des données (FAOSTAT, FOFIFA, etc.)
- Adapte ton langage au niveau d'un agriculteur (pas trop technique)
- Inclus toujours : saison recommandée, sol adapté, rendement estimé quand c'est pertinent
- Si tu ne sais pas, dis-le clairement
- Si c'est une estimation, calcule avec les données fournies et tes connaissances

FORMAT DE RÉPONSE :
📋 **Réponse** (1-3 phrases de synthèse)
📊 **Détails** (liste à puces avec les étapes ou informations)
⚠️ **Attention** (risques ou précautions si applicable)
💡 **Conseil** (astuce pratique)""",

        'en': """You are Dr. Andry Rakoto, an expert agronomist in Madagascar, employed by SmartSaha.
You advise Malagasy farmers on a daily basis.

RULES:
- Respond precisely and practically, adapted to Madagascar's local conditions
- Use bullet points for steps
- Cite sources when using data (FAOSTAT, FOFIFA, etc.)
- Adapt language for farmers (not too technical)
- Always include: recommended season, suitable soil, estimated yield when relevant
- If you don't know, say so clearly

RESPONSE FORMAT:
📋 **Answer** (1-3 summary sentences)
📊 **Details** (bullet points with steps or information)
⚠️ **Warning** (risks or precautions if applicable)
💡 **Tip** (practical advice)""",

        'mg': """Ianao dia Dr. Andry Rakoto, injeniera agronoma manampahaizana ao Madagasikara, mpiasa ao amin'ny SmartSaha.
Manoro hevitra ny tantsaha malagasy isan'andro ianao.

FITSIPIKA:
- Valio tsotra sy azo ampiharina araka ny toe-javatra eto Madagasikara
- Ampiasao ny lisitra ho an'ny dingana tsirairay
- Tanisao ny loharano rehefa mampiasa angon-drakitra (FAOSTAT, FOFIFA, sns.)
- Ampiasao ny fiteny mora azon'ny tantsaha
- Ampidiro foana: vanim-potoana tsara, tany mety, vokatra azo antenaina

ENDRIKA VALINY:
📋 **Valiny** (fintinina 1-3 fehezanteny)
📊 **Antsipirihany** (lisitra misy ny dingana)
⚠️ **Tandremo** (loza na fiarovan-tena)
💡 **Torohevitra** (torohevitra azo ampiharina)""",
    },

    'plantation': {
        'fr': """Tu es Dr. Andry, expert en techniques de plantation à Madagascar.
L'agriculteur te demande des conseils sur le semis ou la plantation.

INCLUS TOUJOURS DANS TA RÉPONSE :
1. La période de semis optimale (mois exact, selon la région si possible)
2. Le type de sol recommandé
3. La préparation du terrain
4. L'espacement et la profondeur de semis
5. Les variétés recommandées (de préférence FOFIFA/locales)
6. Le rendement moyen attendu (données FAOSTAT si disponibles)
7. Les soins post-plantation les plus importants""",

        'en': """You are Dr. Andry, expert in planting techniques in Madagascar.
The farmer asks for planting or sowing advice.

ALWAYS INCLUDE:
1. Optimal sowing period (exact months, region-specific if possible)
2. Recommended soil type
3. Land preparation
4. Spacing and sowing depth
5. Recommended varieties (FOFIFA/local preferred)
6. Expected average yield (FAOSTAT data if available)
7. Most important post-planting care""",

        'mg': """Ianao dia Dr. Andry, manampahaizana momba ny teknikam-pambolena ao Madagasikara.
Ny tantsaha dia mangataka torohevitra momba ny famafy na ny fambolena.

AMPIDIRO FOANA NY VALINY:
1. Fotoana tsara indrindra hamafy (volana marina)
2. Karazana tany tsara
3. Fikarakarana ny tany
4. Elanelana sy halahidin'ny famafy
5. Karazana voly tsara (FOFIFA/eo an-toerana)
6. Vokatra azo antenaina
7. Fikarakarana rehefa vita ny fambolena""",
    },

    'diagnostic': {
        'fr': """Tu es Dr. Andry, phytopathologiste expert à Madagascar.
L'agriculteur décrit un problème sur ses cultures (maladie, ravageur, carence).

DÉMARCHE DE DIAGNOSTIC :
1. Identifie les symptômes clés décrits
2. Propose le(s) diagnostic(s) le(s) plus probable(s) pour Madagascar
3. Explique la cause (champignon, insecte, carence, etc.)
4. Recommande un traitement immédiat (si possible des solutions locales/bio)
5. Propose des mesures préventives pour la prochaine saison
6. Si nécessaire, recommande de consulter un technicien agricole local

IMPORTANT : Privilégie les solutions accessibles localement (neem, cendres, rotation).""",

        'en': """You are Dr. Andry, plant pathology expert in Madagascar.
The farmer describes a crop problem (disease, pest, deficiency).

DIAGNOSTIC APPROACH:
1. Identify key symptoms described
2. Propose most likely diagnosis for Madagascar
3. Explain the cause
4. Recommend immediate treatment (local/bio solutions preferred)
5. Propose preventive measures for next season
6. If needed, recommend consulting local agricultural technician

IMPORTANT: Prioritize locally available solutions (neem, ash, rotation).""",

        'mg': """Ianao dia Dr. Andry, manampahaizana momba ny aretin-javamaniry ao Madagasikara.
Ny tantsaha dia mamaritra olana momba ny voly (aretina, biby mpandravarava, tsy fahampiana).

DINGANA FIZAHANA:
1. Fantaro ny soritr'aretina resahiny
2. Omeo ny antony mety indrindra
3. Hazavao ny fototra (holatra, bibikely, tsy fahampiana, sns.)
4. Torohy ny fitsaboana aingana (vahaolana eo an-toerana/bio)
5. Saraho ny fepetra fisorohana ho an'ny vanim-potoana manaraka
6. Raha ilaina, torohy haka hevitra amin'ny teknisianina""",
    },

    'rendement': {
        'fr': """Tu es Dr. Andry, expert en agronomie de production à Madagascar.
L'agriculteur te pose une question sur les rendements ou la production.

DANS TA RÉPONSE :
1. Donne le rendement moyen national (données FAOSTAT si disponibles)
2. Compare avec le rendement de l'agriculteur si fourni
3. Identifie les facteurs limitants possibles
4. Propose des techniques pour améliorer le rendement
5. Estime la production totale si la superficie est connue
6. Mentionne les meilleures variétés pour maximiser le rendement""",

        'en': """You are Dr. Andry, production agronomy expert in Madagascar.
The farmer asks about yields or production.

IN YOUR RESPONSE:
1. Give national average yield (FAOSTAT data if available)
2. Compare with farmer's yield if provided
3. Identify possible limiting factors
4. Suggest techniques to improve yield
5. Estimate total production if area is known
6. Mention best varieties for maximum yield""",

        'mg': """Ianao dia Dr. Andry, manampahaizana momba ny vokatra fambolena ao Madagasikara.
Ny tantsaha dia manontany momba ny vokatra na ny famokarana.

AO AMIN'NY VALINY:
1. Omeo ny vokatra antonony (angon-drakitra FAOSTAT)
2. Ampitahao amin'ny vokarin'ny tantsaha raha misy
3. Fantaro ny antony mety manapena ny vokatra
4. Torohy teknika hanatsarana ny vokatra
5. Tombanana ny famokarana raha fantatra ny velarana""",
    },

    'meteo': {
        'fr': """Tu es Dr. Andry, agro-climatologue à Madagascar.
L'agriculteur te pose une question sur la météo et son impact sur l'agriculture.

DANS TA RÉPONSE :
1. Interprète les données météo du contexte (si fournies)
2. Évalue l'impact sur les cultures en cours
3. Recommande des actions immédiates si nécessaire
4. Alerte sur les risques climatiques (cyclone, sécheresse, gel)
5. Conseille sur la planification des travaux selon la météo""",

        'en': """You are Dr. Andry, agro-climatologist in Madagascar.
The farmer asks about weather impact on agriculture.

IN YOUR RESPONSE:
1. Interpret weather data from context (if provided)
2. Evaluate impact on current crops
3. Recommend immediate actions if needed
4. Alert about climate risks
5. Advise on work planning according to weather""",

        'mg': """Ianao dia Dr. Andry, manampahaizana momba ny toetrandro sy ny fambolena ao Madagasikara.
Ny tantsaha dia manontany momba ny toetrandro sy ny fiantraikany amin'ny fambolena.

AO AMIN'NY VALINY:
1. Hazavao ny angona toetrandro (raha misy)
2. Tombano ny fiantraikany amin'ny voly ankehitriny
3. Torohy hetsika aingana raha ilaina
4. Ampahafantaro ny loza avy amin'ny toetrandro
5. Torohy fandaminana ny asa araka ny toetrandro""",
    },

    'sol': {
        'fr': """Tu es Dr. Andry, pédologue expert des sols malgaches.
L'agriculteur te pose une question sur le sol, les engrais ou la fertilisation.

DANS TA RÉPONSE :
1. Analyse les données sol du contexte (pH, N, P, K, texture)
2. Interprète les résultats de manière simple
3. Recommande les amendements nécessaires (chaux, fumier, NPK)
4. Donne les doses précises et le timing d'application
5. Privilégie les solutions organiques locales (fumier de zébu, compost)
6. Rappelle l'importance de la matière organique dans les sols malgaches""",

        'en': """You are Dr. Andry, soil science expert for Malagasy soils.
The farmer asks about soil, fertilizers or fertilization.

IN YOUR RESPONSE:
1. Analyze soil data from context (pH, N, P, K, texture)
2. Interpret results simply
3. Recommend necessary amendments
4. Give precise doses and application timing
5. Prioritize local organic solutions
6. Emphasize organic matter importance in Malagasy soils""",

        'mg': """Ianao dia Dr. Andry, manampahaizana momba ny tany malagasy.
Ny tantsaha dia manontany momba ny tany, ny zezika na ny fampitomboana ny tany.

AO AMIN'NY VALINY:
1. Diniho ny angona tany ao amin'ny contexte (pH, N, P, K)
2. Hazavao ny vokany amin'ny fomba tsotra
3. Torohy ny fanitsiana ilaina
4. Omeo ny fatran-javatra marina sy ny fotoana fampiharana
5. Omeo lanja ny vahaolana organika eo an-toerana""",
    },

    'marche': {
        'fr': """Tu es Dr. Andry, également spécialiste en économie agricole à Madagascar.
L'agriculteur pose une question sur les prix, la vente ou le marché.

DANS TA RÉPONSE :
1. Donne des informations sur les prix courants si connus
2. Conseille sur le meilleur moment pour vendre
3. Suggère les circuits de commercialisation (marché local, collecteur, coopérative)
4. Calcule la rentabilité si les données sont suffisantes
5. Mentionne le marketplace SmartSaha pour la vente en ligne""",

        'en': """You are Dr. Andry, also specialist in agricultural economics in Madagascar.
The farmer asks about prices, selling or markets.

IN YOUR RESPONSE:
1. Give current price info if known
2. Advise on best time to sell
3. Suggest marketing channels
4. Calculate profitability if data is sufficient
5. Mention SmartSaha marketplace for online selling""",

        'mg': """Ianao dia Dr. Andry, manampahaizana momba ny toekarena fambolena ao Madagasikara.
Ny tantsaha dia manontany momba ny vidiny, ny fivarotana na ny tsena.

AO AMIN'NY VALINY:
1. Omeo vaovao momba ny vidiny ankehitriny
2. Torohy ny fotoana tsara indrindra hivarotana
3. Torohy ny lalan'ny varotra (tsena eo an-toerana, mpanangona, koperativa)
4. Kajio ny tombony raha ampy ny angona
5. Resaho ny marketplace SmartSaha""",
    },
    'stockage': {
        'fr': """Tu es Dr. Andry, expert en post-récolte à Madagascar.
L'agriculteur pose une question sur le stockage, le séchage ou la conservation.

DANS TA RÉPONSE :
1. Indique le taux d'humidité cible pour le grain concerné
2. Recommande la méthode de séchage adaptée
3. Décris les options de stockage (silo, sacs PICS, grenier amélioré)
4. Alerte sur les risques (insectes, moisissures, rongeurs)
5. Donne les coûts approximatifs si possible""",

        'en': """You are Dr. Andry, post-harvest expert in Madagascar.
The farmer asks about storage, drying or conservation.

IN YOUR RESPONSE:
1. Indicate target moisture content
2. Recommend appropriate drying method
3. Describe storage options
4. Alert about risks
5. Give approximate costs if possible""",

        'mg': """Ianao dia Dr. Andry, manampahaizana momba ny fitehirizana vokatra ao Madagasikara.
Ny tantsaha dia manontany momba ny fitehirizana, ny fanainana na ny fikajiana.

AO AMIN'NY VALINY:
1. Asehoy ny fatra-dranon'ny voa ilaina
2. Torohy ny fomba fanainana mety
3. Tantarao ny safidy fitehirizana
4. Ampahafantaro ny loza (bibikely, holatra, voalavo)
5. Omeo ny vidiny tombanana""",
    },
}


def get_system_prompt(prompt_key: str, language: str) -> str:
    """Retourne le system prompt approprié selon l'intention et la langue."""
    prompts = SYSTEM_PROMPTS.get(prompt_key, SYSTEM_PROMPTS['general'])
    prompt = prompts.get(language, prompts.get('fr', ''))
    lang_instruction = LANGUAGE_INSTRUCTIONS.get(language, LANGUAGE_INSTRUCTIONS['fr'])
    return f"{prompt}\n\n{lang_instruction}"


# ══════════════════════════════════════════════════════════════════════════════
# 1. SimpleAIClient — OpenRouter sans contexte
# ══════════════════════════════════════════════════════════════════════════════
class SimpleAIClient:
    def __init__(self):
        self.api_key = getattr(settings, 'OPENROUTER_API_KEY', None) or os.getenv('OPENROUTER_API_KEY')
        if not self.api_key:
            raise ValueError('OPENROUTER_API_KEY manquant')

        self.base_url = 'https://openrouter.ai/api/v1'
        self.models = [
            'deepseek/deepseek-chat:free',
            'huggingfaceh4/zephyr-7b-beta:free',
            'openchat/openchat-7b:free',
        ]

    def ask(self, question: str, system_prompt: str = None) -> str:
        sys_prompt = system_prompt or get_system_prompt('general', 'fr')
        messages = [
            {'role': 'system', 'content': sys_prompt},
            {'role': 'user', 'content': question},
        ]

        for model in self.models:
            try:
                headers = {
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json',
                    'HTTP-Referer': 'https://localhost',
                    'X-Title': 'SmartSaha',
                }
                payload = {
                    'model': model,
                    'messages': messages,
                    'max_tokens': 1000,
                }
                with httpx.Client(timeout=30.0) as client:
                    response = client.post(f'{self.base_url}/chat/completions', json=payload, headers=headers)
                    if response.status_code == 200:
                        return response.json()['choices'][0]['message']['content']
            except Exception as e:
                print(f'❌ Erreur avec {model}: {e}')

        return "Désolé, le service est temporairement indisponible. Réessaie dans quelques minutes."


# ══════════════════════════════════════════════════════════════════════════════
# 2. RobustGeminiClient — Gemini HTTP direct (sans SDK)
# ══════════════════════════════════════════════════════════════════════════════
class RobustGeminiClient:
    def __init__(self):
        self.api_key = getattr(settings, 'GEMINI_API_KEY', None) or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError('GEMINI_API_KEY manquant')

        self.model = 'gemini-2.0-flash'
        self.base_url = (
            f'https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent'
        )

    def ask(self, question: str, system_prompt: str = None) -> str:
        sys_prompt = system_prompt or get_system_prompt('general', 'fr')
        full_prompt = f'{sys_prompt}\n\n{question}'

        try:
            url = f'{self.base_url}?key={self.api_key}'
            payload = {'contents': [{'parts': [{'text': full_prompt}]}]}
            response = http_requests.post(url, json=payload, headers={'Content-Type': 'application/json'}, timeout=30)

            if response.status_code == 200:
                result = response.json()
                candidates = result.get('candidates', [])
                if candidates:
                    return candidates[0]['content']['parts'][0]['text']
                return 'Erreur: Aucune réponse générée par le modèle'

            error_msg = f'Status {response.status_code}: {response.text}'
            return f'Erreur API Gemini: {error_msg}'

        except http_requests.exceptions.Timeout:
            return 'Erreur: Timeout — API trop lente'
        except Exception as e:
            return f'Erreur: {str(e)}'


# ══════════════════════════════════════════════════════════════════════════════
# 3. MistralAgentClient — Mistral sans contexte
# ══════════════════════════════════════════════════════════════════════════════
class MistralAgentClient:
    def __init__(self):
        self.api_key = getattr(settings, 'MISTRAL_API_KEY', None) or os.getenv('MISTRAL_API_KEY')
        if not self.api_key:
            raise ValueError('MISTRAL_API_KEY manquant')

        try:
            try:
                from mistralai import Mistral # noqa: F401
            except ImportError:
                from mistralai.client import Mistral # noqa: F401
            self.mistral_available = True
        except (ImportError, AttributeError, TypeError):
            self.mistral_available = False
            print("WARNING: Mistral SDK non disponible (Agent)")

    def ask(self, question: str, system_prompt: str = None) -> str:
        if not self.mistral_available:
            return 'Erreur: pip install mistralai'

        sys_prompt = system_prompt or get_system_prompt('general', 'fr')

        try:
            try:
                from mistralai import Mistral
            except ImportError:
                from mistralai.client import Mistral

            with Mistral(api_key=self.api_key) as client:
                response = client.chat.complete(
                    model='mistral-small-latest',
                    messages=[
                        {'role': 'system', 'content': sys_prompt},
                        {'role': 'user', 'content': question},
                    ],
                    max_tokens=1000,
                    temperature=0.3,
                    stream=False,
                )

            return response.choices[0].message.content

        except Exception as e:
            return f'Erreur service: {str(e)}'


# ══════════════════════════════════════════════════════════════════════════════
# 4. DeepSeekClient — OpenRouter avec contexte parcel
# ══════════════════════════════════════════════════════════════════════════════
class DeepSeekClient:
    def __init__(self, model='deepseek/deepseek-r1:free'):
        self.api_key = getattr(settings, 'OPENROUTER_API_KEY', None) or os.getenv('OPENROUTER_API_KEY')
        if not self.api_key:
            raise ValueError('OPENROUTER_API_KEY manquant dans settings ou .env')

        self.base_url = 'https://openrouter.ai/api/v1'
        self.model = model

    def ask(self, question: str, parcel_uuid: str = None, user_modules: dict = None,
            system_prompt: str = None) -> str:
        context_data = ContextBuilder.build_context(parcel_uuid, user_modules)
        sys_prompt = system_prompt or get_system_prompt('general', 'fr')
        full_prompt = f'{sys_prompt}\n\nDonnées locales:\n{context_data}\n\nQuestion: {question}\nRéponse:'

        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }
        payload = {
            'model': self.model,
            'messages': [{'role': 'user', 'content': full_prompt}],
        }

        with httpx.Client(timeout=60.0) as client:
            try:
                response = client.post(f'{self.base_url}/chat/completions', json=payload, headers=headers)
                response.raise_for_status()
                return response.json()['choices'][0]['message']['content']
            except httpx.HTTPStatusError as e:
                return f'Erreur API OpenRouter ({e.response.status_code}): {e.response.text}'
            except Exception as e:
                return f'Erreur interne: {str(e)}'


# ══════════════════════════════════════════════════════════════════════════════
# 5. GeminiClient — SDK genai avec contexte parcel
# ══════════════════════════════════════════════════════════════════════════════
class GeminiClient:
    def __init__(self, model='google/gemini-2.0-flash-exp:free'):
        self.api_key = getattr(settings, 'GEMINI_API_KEY', None) or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError('GEMINI_API_KEY manquant dans settings ou .env')

        self.model = model
        try:
            from google import genai
            self.client = genai.Client(api_key=self.api_key)
            self.sdk_available = True
        except ImportError:
            self.sdk_available = False

    def ask(self, question: str, parcel_uuid: str = None, user_modules: dict = None,
            system_prompt: str = None) -> str:
        if not self.sdk_available:
            return 'Erreur: pip install google-genai'

        context_data = ContextBuilder.build_context(parcel_uuid, user_modules)
        sys_prompt = system_prompt or get_system_prompt('general', 'fr')
        full_prompt = f'{sys_prompt}\n\nDonnées locales:\n{context_data}\n\nQuestion: {question}\nRéponse:'

        try:
            from google import genai
            response = self.client.models.generate_content(model=self.model, contents=full_prompt)
            return response.text
        except Exception as e:
            return f'Erreur API Gemini: {str(e)}'


# ══════════════════════════════════════════════════════════════════════════════
# 6. WorkingAIClient — OpenRouter multi-modèles avec fallback
# ══════════════════════════════════════════════════════════════════════════════
class WorkingAIClient:
    def __init__(self):
        self.models = [
            'anthropic/claude-3-haiku:free',
            'google/gemini-2.0-flash-exp:free',
            'meta-llama/llama-3.1-8b-instruct:free',
            'microsoft/wizardlm-2-8x22b:free',
        ]

    def ask(self, question: str, parcel_uuid: str = None, user_modules: dict = None,
            system_prompt: str = None) -> str:
        context_data = ContextBuilder.build_context(parcel_uuid, user_modules)
        sys_prompt = system_prompt or get_system_prompt('general', 'fr')
        full_prompt = f'{sys_prompt}\n\nDonnées locales:\n{context_data}\n\nQuestion: {question}\nRéponse:'

        api_key = getattr(settings, 'OPENROUTER_API_KEY', None) or os.getenv('OPENROUTER_API_KEY')

        for model in self.models:
            try:
                headers = {
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json',
                }
                payload = {
                    'model': model,
                    'messages': [{'role': 'user', 'content': full_prompt}],
                }
                with httpx.Client(timeout=60.0) as client:
                    response = client.post(
                        'https://openrouter.ai/api/v1/chat/completions',
                        json=payload,
                        headers=headers,
                    )
                    if response.status_code == 200:
                        return response.json()['choices'][0]['message']['content']
            except Exception as e:
                print(f'ERROR: Erreur avec {model}: {e}')

        return 'Désolé, tous les services IA sont temporairement saturés. Réessaie dans 1-2 minutes.'


# ══════════════════════════════════════════════════════════════════════════════
# 7. MistralRAGClient — Mistral avec contexte parcel (RAG)
# ══════════════════════════════════════════════════════════════════════════════
class MistralRAGClient:
    def __init__(self, model='mistral-medium'):
        self.api_key = getattr(settings, 'MISTRAL_API_KEY', None) or os.getenv('MISTRAL_API_KEY')
        if not self.api_key:
            raise ValueError('MISTRAL_API_KEY manquant dans settings ou .env')

        self.model = model
        try:
            try:
                from mistralai import Mistral # noqa: F401
            except ImportError:
                from mistralai.client import Mistral # noqa: F401
            self.mistral_available = True
        except (ImportError, AttributeError, TypeError):
            self.mistral_available = False
            print("WARNING: Mistral SDK non disponible (RAG)")

    def ask(self, question: str, parcel_uuid: str = None, user_modules: dict = None,
            system_prompt: str = None, chat_history: list = None,
            knowledge_query: str = None, crop_name: str = None) -> str:
        if not self.mistral_available:
            return "Erreur: Package 'mistralai' non installé. Exécutez: pip install mistralai"

        context_data = ContextBuilder.build_context(
            parcel_uuid=parcel_uuid,
            user_modules=user_modules,
            chat_history=chat_history,
            knowledge_query=knowledge_query or question,
            crop_name=crop_name,
        )

        sys_prompt = system_prompt or get_system_prompt('general', 'fr')

        full_prompt = f"""
CONTEXTE LOCAL ET DONNÉES UTILISATEUR:
{context_data}

QUESTION À RÉSOUDRE:
{question}

BASÉ SUR LE CONTEXTE CI-DESSUS, RÉPONDS DE MANIÈRE PRÉCISE ET ADAPTÉE :
"""
        try:
            try:
                from mistralai import Mistral
            except ImportError:
                from mistralai.client import Mistral

            with Mistral(api_key=self.api_key) as client:
                response = client.chat.complete(
                    model=self.model,
                    messages=[
                        {'role': 'system', 'content': sys_prompt},
                        {'role': 'user', 'content': full_prompt},
                    ],
                    temperature=0.3,
                    max_tokens=1500,
                    stream=False,
                )

            return response.choices[0].message.content

        except Exception as e:
            error_msg = f'Erreur API Mistral: {str(e)}'
            print(f'ERROR: {error_msg}')
            return error_msg


# ══════════════════════════════════════════════════════════════════════════════
# 8. SmartAssistant — ★ Orchestrateur intelligent (NOUVEAU)
# ══════════════════════════════════════════════════════════════════════════════
class SmartAssistant:
    """
    Orchestrateur intelligent qui combine :
    - Détection d'intention et de langue
    - Routage vers le meilleur modèle
    - Contexte RAG enrichi (parcelle + KB + FAOSTAT + historique)
    - Fallback automatique entre providers
    - Suivi des performances

    C'est le point d'entrée principal pour les nouvelles vues.
    """

    def __init__(self):
        self._router = IntelligentRouter()
        self._intent_detector = IntentDetector()
        self._clients = {}

    def _get_client(self, provider: str):
        """Lazy-init des clients IA."""
        if provider not in self._clients:
            try:
                if provider == 'gemini':
                    self._clients[provider] = RobustGeminiClient()
                elif provider == 'mistral':
                    self._clients[provider] = MistralAgentClient()
                elif provider == 'mistral_rag':
                    self._clients[provider] = MistralRAGClient()
                elif provider == 'deepseek':
                    self._clients[provider] = DeepSeekClient()
                elif provider == 'openrouter':
                    self._clients[provider] = SimpleAIClient()
                else:
                    self._clients[provider] = RobustGeminiClient()
            except Exception as e:
                print(f"⚠️ Impossible d'initialiser {provider}: {e}")
                return None
        return self._clients.get(provider)

    def ask(
        self,
        question: str,
        parcel_uuid: str = None,
        user_modules: dict = None,
        chat_history: list = None,
        crop_name: str = None,
        user=None,
        preferred_provider: str = None,
    ) -> dict:
        """
        Point d'entrée intelligent pour poser une question.

        Returns:
            {
                'answer': str,
                'intent': str,
                'language': str,
                'provider': str,
                'model': str,
                'response_time_ms': int,
                'context_used': bool,
            }
        """
        start_time = time.time()

        # 1. Analyser la question (intention + langue)
        analysis = self._intent_detector.analyze(question)
        language = analysis['language']
        prompt_key = analysis['prompt_key']

        # 2. Construire le contexte enrichi
        context_data = ContextBuilder.build_context(
            parcel_uuid=parcel_uuid,
            user_modules=user_modules,
            chat_history=chat_history,
            knowledge_query=question,
            crop_name=crop_name,
            user=user,
        )

        # 3. Router vers le meilleur modèle
        route = self._router.route(
            question=question,
            context_size=len(context_data),
            preferred_provider=preferred_provider,
        )

        # 4. Construire le prompt final
        system_prompt = get_system_prompt(prompt_key, language)

        if context_data:
            full_question = f"DONNÉES CONTEXTUELLES:\n{context_data}\n\nQUESTION:\n{question}"
        else:
            full_question = question

        # 5. Appeler le modèle avec fallback
        answer = None
        used_provider = route['provider']
        used_model = route['model']

        # Essayer le provider principal
        client = self._get_client(route['provider'])
        if client:
            try:
                answer = client.ask(
                    question=full_question,
                    system_prompt=system_prompt,
                )
                if answer and 'Erreur' not in answer[:20]:
                    self._router.mark_success(route['provider'])
                else:
                    raise Exception(f"Réponse erreur: {answer[:50]}")
            except Exception as e:
                print(f"⚠️ {route['provider']} échoué: {e}")
                self._router.mark_failure(route['provider'])
                answer = None

        # Fallback si nécessaire
        if not answer or 'Erreur' in answer[:20]:
            for fallback in self._router.get_fallback_chain(route['provider']):
                fb_client = self._get_client(fallback['name'])
                if fb_client:
                    try:
                        answer = fb_client.ask(
                            question=full_question,
                            system_prompt=system_prompt,
                        )
                        if answer and 'Erreur' not in answer[:20]:
                            used_provider = fallback['name']
                            used_model = fallback['model']
                            self._router.mark_success(fallback['name'])
                            break
                    except Exception:
                        self._router.mark_failure(fallback['name'])
                        continue

        # Dernier recours
        if not answer:
            answer = self._get_fallback_response(question, language)
            used_provider = 'fallback_local'
            used_model = 'none'

        elapsed_ms = int((time.time() - start_time) * 1000)

        return {
            'answer': answer,
            'intent': analysis['intent'],
            'language': language,
            'provider': used_provider,
            'model': used_model,
            'response_time_ms': elapsed_ms,
            'context_used': bool(context_data),
            'confidence': analysis['confidence'],
        }

    @staticmethod
    def _get_fallback_response(question: str, language: str) -> str:
        """Réponses de fallback locales quand tous les services IA sont indisponibles."""
        fallbacks = {
            'fr': {
                'riz': 'À Madagascar, plantez le riz en novembre-décembre (saison Asara). Rendement moyen national : 2 472 kg/ha (FAOSTAT 2023).',
                'mais': 'Maïs : plantation octobre-novembre. Cycle 90-120 jours. Rendement national : 1 810 kg/ha (FAOSTAT).',
                'manioc': 'Manioc : tolérant aux sols pauvres. Plantation octobre-décembre. Rendement : 7 771 kg/ha (FAOSTAT).',
                'haricot': 'Haricot : fixe l\'azote. Excellente rotation avec les céréales. Rendement : 1 199 kg/ha.',
                'default': 'Service IA temporairement indisponible. Votre question a été enregistrée.',
            },
            'en': {
                'rice': 'In Madagascar, plant rice in November-December (Asara season). National average yield: 2,472 kg/ha (FAOSTAT 2023).',
                'default': 'AI service temporarily unavailable. Your question has been recorded.',
            },
            'mg': {
                'vary': 'Ao Madagasikara, amboleo ny vary amin\'ny volana novambra-desambra (Asara). Vokatra antonony: 2 472 kg/ha (FAOSTAT 2023).',
                'default': 'Tsy afaka ny serivisy IA amin\'izao fotoana izao. Voatahiry ny fanontanianao.',
            },
        }

        lang_fallbacks = fallbacks.get(language, fallbacks['fr'])
        q_lower = question.lower()

        for key, response in lang_fallbacks.items():
            if key != 'default' and key in q_lower:
                return response

        return lang_fallbacks.get('default', fallbacks['fr']['default'])
