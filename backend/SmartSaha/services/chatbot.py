# SmartSaha/services/simple_ai_client.py
import os
import httpx
from django.conf import settings
from mistralai import Mistral

BASE_PROMPT = """
Tu es un ingenieur agronome expert à Madagascar.
Reponds toujours de maniere précise, pratique, court et adaptee aux conditions locales :
- Inclue les saisons, sols et pratiques agricoles typiques.
- Ne donne jamais de reponses vagues.
- Si tu ne sais pas, indique clairement que l’information n’est pas disponible.
"""


class SimpleAIClient:
    def __init__(self):
        self.api_key = getattr(settings, "OPENROUTER_API_KEY", None) or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY manquant")

        self.base_url = "https://openrouter.ai/api/v1"
        self.models = [
            "deepseek/deepseek-chat:free",
            "huggingfaceh4/zephyr-7b-beta:free",
            "openchat/openchat-7b:free",
        ]

    def ask(self, question: str):
        """Version ultra-simplifiée - utilise seulement la question de l'utilisateur"""
        full_prompt = f"{BASE_PROMPT}\n\nQuestion: {question}\nRéponse:"

        for model in self.models:
            try:
                print(f"🔄 Essai avec: {model}")

                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://localhost",
                    "X-Title": "SmartSaha"
                }
                payload = {
                    "model": model,
                    "messages": [{"role": "user", "content": full_prompt}],
                    "max_tokens": 1000
                }

                with httpx.Client(timeout=30.0) as client:
                    response = client.post(
                        f"{self.base_url}/chat/completions",
                        json=payload,
                        headers=headers
                    )

                    if response.status_code == 200:
                        data = response.json()
                        print(f"✅ Succès avec {model}")
                        return data["choices"][0]["message"]["content"]
                    else:
                        print(f"❌ {model} échoué: {response.status_code}")
                        continue

            except Exception as e:
                print(f"❌ Erreur avec {model}: {e}")
                continue

        return "Désolé, le service est temporairement indisponible. Réessaie dans quelques minutes."


# SmartSaha/services/robust_gemini_client.py
from google import genai

BASE_PROMPT = """
Tu es un ingenieur agronome expert à Madagascar.
Reponds toujours de maniere précise, pratique, court et adaptee aux conditions locales :
- Inclue les saisons, sols et pratiques agricoles typiques.
- Ne donne jamais de reponses vagues.
- Si tu ne sais pas, indique clairement que l’information n’est pas disponible.
"""

import requests


class RobustGeminiClient:
    def __init__(self):
        self.api_key = getattr(settings, "GEMINI_API_KEY", None) or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY manquant")

        # 🎯 UNIQUEMENT le modèle de votre URL
        self.model = "gemini-2.0-flash"
        self.base_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"

    def ask(self, question: str):
        """Utilise uniquement le modèle gemini-2.0-flash"""
        full_prompt = f"{BASE_PROMPT}\n\nQuestion: {question}\nRéponse:"

        try:
            print(f"🔄 Appel Gemini avec: {self.model}")

            # Construction de l'URL avec la clé
            url = f"{self.base_url}?key={self.api_key}"

            # Préparation des données
            payload = {
                "contents": [{
                    "parts": [{
                        "text": full_prompt
                    }]
                }]
            }

            # Headers
            headers = {
                "Content-Type": "application/json"
            }

            # Appel API - ICI on utilise requests qui est maintenant importé
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=30
            )

            # Vérification de la réponse
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Succès avec {self.model}")

                # Extraction du texte de réponse
                if "candidates" in result and len(result["candidates"]) > 0:
                    text = result["candidates"][0]["content"]["parts"][0]["text"]
                    return text
                else:
                    return "Erreur: Aucune réponse générée par le modèle"

            else:
                error_msg = f"Status {response.status_code}: {response.text}"
                print(f"❌ {self.model} échoué: {error_msg}")
                return f"Erreur API Gemini: {error_msg}"

        except requests.exceptions.Timeout:
            error_msg = "Timeout - API trop lente"
            print(f"⏰ {error_msg}")
            return f"Erreur: {error_msg}"
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Erreur avec {self.model}: {error_msg}")
            return f"Erreur: {error_msg}"


# # ✅ Utilisation simple
# try:
#     gemini_client = RobustGeminiClient()
#     reponse = gemini_client.ask("Quand planter du riz à Madagascar ?")
#     print(reponse)
# except Exception as e:
#     print(f"Erreur initialisation: {e}")

class MistralAgentClient:
    def __init__(self):
        self.api_key = getattr(settings, "MISTRAL_API_KEY", None) or os.getenv("MISTRAL_API_KEY")

        if not self.api_key:
            raise ValueError("MISTRAL_API_KEY manquant")

        try:
            from mistralai import Mistral
            self.mistral_available = True
        except ImportError:
            self.mistral_available = False

    def ask(self, question: str):
        """Client agronome avec modèle officiel"""
        if not self.mistral_available:
            return "Erreur: pip install mistralai"

        try:
            print(f"🔄 Mistral - Question: {question[:50]}...")

            with  Mistral(api_key=self.api_key) as client:
                response = client.chat.complete(
                    model="mistral-small-latest",  # Modèle gratuit et efficace
                    messages=[
                        {
                            "role": "system",
                            "content": "Expert agronome malgache. Réponses courtes, précises, adaptées aux saisons et sols locaux. Pas de généralités."
                        },
                        {
                            "role": "user",
                            "content": question
                        }
                    ],
                    max_tokens=500,  # Réponses courtes
                    temperature=0.3,  # Réponses précises
                    stream=False
                )

            answer = response.choices[0].message.content
            print(f"✅ Réponse reçue: {answer[:50]}...")
            return answer

        except Exception as e:
            print(f"❌ Erreur Mistral: {e}")
            return f"Erreur service: {str(e)}"