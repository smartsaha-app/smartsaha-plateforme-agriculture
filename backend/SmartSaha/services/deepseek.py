# import httpx
# import os
# from django.conf import settings

# from SmartSaha.services.context_builder import ContextBuilder

# BASE_PROMPT = """
# Tu es un ingenieur agronome expert à Madagascar.
# Reponds toujours de maniere précise, pratique, court et adaptee aux conditions locales :
# - Inclue les saisons, sols et pratiques agricoles typiques.
# - Ne donne jamais de reponses vagues.
# - si cest un estimation, calcule avec les donnees qu on te fourni et tes connaissances
# - Si tu ne sais pas, indique clairement que l’information n’est pas disponible.
# """
# class DeepSeekClient:
#     def __init__(self, model="deepseek/deepseek-r1:free"):
#         self.api_key = getattr(settings, "OPENROUTER_API_KEY", None) or os.getenv("OPENROUTER_API_KEY")
#         if not self.api_key:
#             raise ValueError("OPENROUTER_API_KEY manquant dans settings ou .env")

#         self.base_url = "https://openrouter.ai/api/v1"
#         self.model = model

#     def ask(self, question: str, parcel_uuid: str = None, user_modules: dict = None):
#         context_data = ContextBuilder.build_context(parcel_uuid, user_modules)
#         print(context_data)
#         full_prompt = f"{BASE_PROMPT}\n\nDonnées locales:\n{context_data}\n\nQuestion: {question}\nRéponse:"
#         print(full_prompt)
#         print("OPENROUTER_API_KEY =", self.api_key)

#         headers = {
#             "Authorization": f"Bearer {self.api_key}",
#             "Content-Type": "application/json"
#         }
#         payload = {
#             "model": self.model,
#             "messages": [{"role": "user", "content": full_prompt}]
#         }

#         with httpx.Client(timeout=60.0) as client:
#             try:
#                 response = client.post(f"{self.base_url}/chat/completions", json=payload, headers=headers)
#                 print("Status:", response.status_code)
#                 print("Response:", response.text[:500])  # debug rapide
#                 response.raise_for_status()
#                 data = response.json()
#             except httpx.HTTPStatusError as e:
#                 return f"Erreur API OpenRouter ({e.response.status_code}): {e.response.text}"
#             except Exception as e:
#                 return f"Erreur interne: {str(e)}"

#         # Retourne le contenu de la réponse
#         try:
#             return data["choices"][0]["message"]["content"]
#         except (KeyError, IndexError):
#             return "Aucune réponse reçue du modèle."


# import os
# from django.conf import settings
# from google import genai

# from SmartSaha.services.context_builder import ContextBuilder


# class GeminiClient:
#     def __init__(self, model="google/gemini-2.0-flash-exp:free"):
#         self.api_key = getattr(settings, "GEMINI_API_KEY", None) or os.getenv("GEMINI_API_KEY")
#         if not self.api_key:
#             raise ValueError("GEMINI_API_KEY manquant dans settings ou .env")

#         self.model = model
#         self.client = genai.Client(api_key=self.api_key)

#     def ask(self, question: str, parcel_uuid: str = None, user_modules: dict = None):
#         context_data = ContextBuilder.build_context(parcel_uuid, user_modules)
#         print(context_data)

#         full_prompt = f"{BASE_PROMPT}\n\nDonnées locales:\n{context_data}\n\nQuestion: {question}\nRéponse:"
#         print(full_prompt)
#         print("GEMINI_API_KEY =", self.api_key[:10] + "...")  # Sécurité : n'affiche pas toute la clé

#         try:
#             response = self.client.models.generate_content(
#                 model=self.model,
#                 contents=full_prompt
#             )
#             print("Réponse Gemini reçue")
#             return response.text

#         except Exception as e:
#             return f"Erreur API Gemini: {str(e)}"

# class WorkingAIClient:
#     def __init__(self):
#         # Liste de modèles gratuits qui marchent sur OpenRouter
#         self.models = [
#             "anthropic/claude-3-haiku:free",  # 🥇 Premier choix
#             "google/gemini-2.0-flash-exp:free",  # 🥈 Deuxième choix
#             "meta-llama/llama-3.1-8b-instruct:free",  # 🥉 Troisième choix
#             "microsoft/wizardlm-2-8x22b:free"  # 💪 Backup
#         ]

#     def ask(self, question, parcel_uuid=None, user_modules=None):
#         # 1. Récupère le contexte (comme avant)
#         context_data = ContextBuilder.build_context(parcel_uuid, user_modules)
#         full_prompt = f"{BASE_PROMPT}\n\nDonnées locales:\n{context_data}\n\nQuestion: {question}\nRéponse:"

#         # 2. Essaie chaque modèle jusqu'à ce qu'un marche
#         for model in self.models:
#             try:
#                 print(f"🔄 Essai avec le modèle: {model}")

#                 headers = {
#                     "Authorization": f"Bearer {getattr(settings, "OPENROUTER_API_KEY", None) or os.getenv("OPENROUTER_API_KEY")}",
#                     "Content-Type": "application/json"
#                 }
#                 payload = {
#                     "model": model,
#                     "messages": [{"role": "user", "content": full_prompt}]
#                 }

#                 # 3. Appel API
#                 with httpx.Client(timeout=60.0) as client:
#                     response = client.post(
#                         "https://openrouter.ai/api/v1/chat/completions",
#                         json=payload,
#                         headers=headers
#                     )

#                     if response.status_code == 200:
#                         data = response.json()
#                         print(f"✅ Succès avec {model}")
#                         return data["choices"][0]["message"]["content"]
#                     else:
#                         print(f"❌ {model} a échoué: {response.status_code}")
#                         continue

#             except Exception as e:
#                 print(f"❌ Erreur avec {model}: {e}")
#                 continue

#         # 4. Si tout échoue
#         return "Désolé, tous les services IA sont temporairement saturés. Réessaie dans 1-2 minutes."


# class MistralRAGClient:
#     def __init__(self, model="mistral-medium"):
#         self.api_key = getattr(settings, "MISTRAL_API_KEY", None) or os.getenv("MISTRAL_API_KEY")
#         if not self.api_key:
#             raise ValueError("MISTRAL_API_KEY manquant dans settings ou .env")

#         self.model = model
#         try:
#             from mistralai import Mistral
#             self.mistral_available = True
#         except ImportError:
#             self.mistral_available = False

#     def ask(self, question: str, parcel_uuid: str = None, user_modules: dict = None):
#         """Version RAG avec contexte local"""
#         if not self.mistral_available:
#             return "Erreur: Package 'mistralai' non installé. Exécutez: pip install mistralai"

#         # Construction du contexte RAG
#         context_data = ContextBuilder.build_context(parcel_uuid, user_modules)
#         print("Contexte RAG:", context_data)

#         # Prompt RAG complet
#         full_prompt = f"""
# {BASE_PROMPT}

# CONTEXTE LOCAL ET DONNÉES UTILISATEUR:
# {context_data}

# QUESTION À RÉSOUDRE:
# {question}

# BASÉ SUR LE CONTEXTE CI-DESSUS, RÉPONDS DE MANIÈRE PRÉCISE ET ADAPTÉE :
# """
#         print("Prompt Mistral RAG généré")
#         print("MISTRAL_API_KEY =", self.api_key[:10] + "...")

#         try:
#             from mistralai import Mistral

#             with Mistral(api_key=self.api_key) as client:
#                 response = client.chat.complete(
#                     model=self.model,
#                     messages=[
#                         {
#                             "role": "system",
#                             "content": "Tu es Dr. Andry Rakoto, expert agronome malgache. Réponses courtes, précises, basées sur les données fournies."
#                         },
#                         {
#                             "role": "user",
#                             "content": full_prompt
#                         }
#                     ],
#                     temperature=0.3,  # Réponses précises
#                     max_tokens=1000,
#                     stream=False
#                 )

#             print("Réponse Mistral RAG reçue")
#             return response.choices[0].message.content

#         except Exception as e:
#             error_msg = f"Erreur API Mistral: {str(e)}"
#             print(f"❌ {error_msg}")
#             return error_msg