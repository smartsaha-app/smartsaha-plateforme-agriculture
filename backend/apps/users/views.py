"""
apps/users/views.py
-------------------
Vues d'authentification : signup, login, Google OAuth, reset password.
"""
import secrets
import random
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.core.cache import cache
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import generics, status, viewsets, permissions, filters
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
import threading


from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.core.mixins import BaseModelViewSet, CacheInvalidationMixin
from apps.users.models import User
from apps.users.serializers import (
    UserSerializer, UserSignupSerializer, UserLoginSerializer,
    FarmerDirectorySerializer, MobileSignupSerializer
)

from google.oauth2 import id_token
from google.auth.transport import requests
from django.utils.decorators import method_decorator

token_generator = PasswordResetTokenGenerator()


# ────────────────────────────────────────────────
# Users
# ────────────────────────────────────────────────

@method_decorator(name='list',         decorator=swagger_auto_schema(tags=['Utilisateurs']))
@method_decorator(name='retrieve',     decorator=swagger_auto_schema(tags=['Utilisateurs']))
@method_decorator(name='create',       decorator=swagger_auto_schema(tags=['Utilisateurs']))
@method_decorator(name='update',       decorator=swagger_auto_schema(tags=['Utilisateurs']))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(tags=['Utilisateurs']))
@method_decorator(name='destroy',      decorator=swagger_auto_schema(tags=['Utilisateurs']))
class UserViewSet(CacheInvalidationMixin, BaseModelViewSet):
    queryset           = User.objects.all().prefetch_related('organisations_created')
    serializer_class   = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    cache_prefix       = 'user'


# ────────────────────────────────────────────────
# Auth
# ────────────────────────────────────────────────

@swagger_auto_schema(tags=['Authentification'], operation_summary="Inscription nouvel utilisateur")
class SignupView(generics.CreateAPIView):
    queryset           = User.objects.all()
    serializer_class   = UserSignupSerializer
    permission_classes = []


@swagger_auto_schema(tags=['Authentification'])
class LoginView(APIView):
    permission_classes = []

    @swagger_auto_schema(
        operation_summary="Authentification Utilisateur",
        tags=['Authentification'],
        request_body=UserLoginSerializer,
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'token': openapi.Schema(type=openapi.TYPE_STRING),
                    'user': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'uuid':       openapi.Schema(type=openapi.TYPE_STRING),
                            'username':   openapi.Schema(type=openapi.TYPE_STRING),
                            'email':      openapi.Schema(type=openapi.TYPE_STRING),
                            'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                            'last_name':  openapi.Schema(type=openapi.TYPE_STRING),
                            'role':       openapi.Schema(type=openapi.TYPE_STRING),
                            'is_staff':   openapi.Schema(type=openapi.TYPE_BOOLEAN),
                            'spaces': openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'agriculture':  openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                    'organisation': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                    'superviseur':  openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                }
                            ),
                        }
                    )
                }
            )
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response = Response({
            'user': {
                'uuid':       str(user.uuid),
                'username':   user.username,
                'email':      user.email,
                'first_name': user.first_name,
                'last_name':  user.last_name,
                'role':       user.role,
                'is_staff':   user.is_staff,
                'spaces':     user.get_spaces(),
            },
        }, status=status.HTTP_200_OK)

        # Retrieve SIMPLE_JWT settings
        sjwt_settings = getattr(settings, 'SIMPLE_JWT', {})
        access_cookie_name = sjwt_settings.get('AUTH_COOKIE', 'access_token')
        refresh_cookie_name = sjwt_settings.get('REFRESH_COOKIE', 'refresh_token')

        samesite_policy = 'None' if not settings.DEBUG else 'Lax'

        response.set_cookie(
            access_cookie_name,
            access_token,
            httponly=True,
            secure=not settings.DEBUG,
            samesite=samesite_policy,
            max_age=60*60*24*7  # 7 jours
        )
        response.set_cookie(
            refresh_cookie_name,
            refresh_token,
            httponly=True,
            secure=not settings.DEBUG,
            samesite=samesite_policy,
            max_age=60*60*24*7
        )
        response.set_cookie(
            'is_logged_in',
            'true',
            httponly=False,  # Accessible par le JS pour savoir si l'utilisateur est connecté
            secure=not settings.DEBUG,
            samesite=samesite_policy,
            max_age=60*60*24*7
        )
        return response


@swagger_auto_schema(tags=['Authentification'])
class LogoutView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_summary="Déconnexion Utilisateur",
        tags=['Authentification'],
        responses={200: openapi.Schema(type=openapi.TYPE_OBJECT, properties={'message': openapi.Schema(type=openapi.TYPE_STRING)})}
    )
    def post(self, request):
        response = Response({'message': 'Déconnecté avec succès'}, status=status.HTTP_200_OK)
        # On supprime les cookies
        sjwt_settings = getattr(settings, 'SIMPLE_JWT', {})
        access_cookie_name = sjwt_settings.get('AUTH_COOKIE', 'access_token')
        refresh_cookie_name = sjwt_settings.get('REFRESH_COOKIE', 'refresh_token')
        
        samesite_policy = 'None' if not settings.DEBUG else 'Lax'
        response.delete_cookie(access_cookie_name, samesite=samesite_policy)
        response.delete_cookie(refresh_cookie_name, samesite=samesite_policy)
        response.delete_cookie('is_logged_in', samesite=samesite_policy)
        return response


@swagger_auto_schema(tags=['Authentification'])
class ForgotPasswordView(APIView):
    permission_classes = []

    @swagger_auto_schema(
        operation_summary="Mot de passe oublié",
        tags=['Authentification'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL)
            }
        ),
        responses={
            200: openapi.Schema(type=openapi.TYPE_OBJECT, properties={'message': openapi.Schema(type=openapi.TYPE_STRING)}),
            400: "Email requis"
        }
    )
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email requis'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': "Si l'email existe, un lien a été envoyé"}, status=status.HTTP_200_OK)

        uid   = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)
        frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')
        reset_link   = f"{frontend_url}/reset-password/{uid}/{token}/"

        try:
            send_mail(
                subject="Réinitialisation de votre mot de passe - SmartSaha",
                message=f"Cliquez sur ce lien pour réinitialiser votre mot de passe :\n{reset_link}\n\nCe lien expire dans 24h.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            return Response({'message': 'Lien de réinitialisation envoyé par email'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'error': "Erreur lors de l'envoi de l'email"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(tags=['Authentification'])
class ResetPasswordView(APIView):
    permission_classes = []

    @swagger_auto_schema(
        operation_summary="Réinitialisation du mot de passe",
        tags=['Authentification'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['new_password', 'confirm_password'],
            properties={
                'new_password':     openapi.Schema(type=openapi.TYPE_STRING),
                'confirm_password': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={
            200: openapi.Schema(type=openapi.TYPE_OBJECT, properties={'message': openapi.Schema(type=openapi.TYPE_STRING)}),
            400: "Lien invalide ou expiré"
        }
    )
    def post(self, request, uidb64, token):
        try:
            uid  = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'error': 'Lien invalide ou expiré'}, status=400)

        if not token_generator.check_token(user, token):
            return Response({'error': 'Lien invalide ou expiré'}, status=400)

        new_pw  = request.data.get('new_password')
        conf_pw = request.data.get('confirm_password')

        if not new_pw:
            return Response({'error': 'Mot de passe requis'}, status=400)
        if new_pw != conf_pw:
            return Response({'error': 'Les mots de passe ne correspondent pas'}, status=400)
        if len(new_pw) < 8:
            return Response({'error': 'Minimum 8 caractères'}, status=400)

        user.set_password(new_pw)
        user.save()
        return Response({'message': 'Mot de passe réinitialisé avec succès'})


@swagger_auto_schema(tags=['Authentification'])
class GoogleLoginView(APIView):
    permission_classes = []
    GOOGLE_CLIENT_ID   = "186820827638-9915pmkfj0s6ch5tdrc73vakoep2vlsd.apps.googleusercontent.com"

    @swagger_auto_schema(
        operation_summary="Connexion avec Google OAuth",
        tags=['Authentification'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['token', 'role'],
            properties={
                'token': openapi.Schema(type=openapi.TYPE_STRING),
                'role':  openapi.Schema(type=openapi.TYPE_STRING, description="Obligatoire si nouvel utilisateur")
            }
        ),
        responses={200: "Voir structure LoginView", 400: "Token ou rôle manquant/invalide"}
    )
    def post(self, request, *args, **kwargs):
        token_from_front = request.data.get('token')
        role_from_front = request.data.get('role')
        
        if not token_from_front:
            return Response({'error': 'Token missing'}, status=400)
            
        try:
            idinfo = id_token.verify_oauth2_token(
                token_from_front, requests.Request(), self.GOOGLE_CLIENT_ID
            )
            email = idinfo.get('email')
            if not email:
                return Response({'error': 'Email not provided by Google'}, status=400)

            # Vérification de l'existence de l'utilisateur avant création
            user_exists = User.objects.filter(email=email).exists()
            
            if not user_exists:
                if not role_from_front:
                    return Response({'error': 'Role is required for new accounts'}, status=400)
                
                valid_roles = [c[0] for c in User.ROLE_CHOICES]
                if role_from_front not in valid_roles:
                    return Response({'error': 'Invalid role provided'}, status=400)

            user, _ = User.objects.get_or_create(
                email=email,
                defaults={
                    'username':   email,
                    'first_name': idinfo.get('given_name', ''),
                    'last_name':  idinfo.get('family_name', ''),
                    'password':   secrets.token_urlsafe(16),
                    'role':       role_from_front,
                }
            )
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            response = Response({
                'user': {
                    'uuid':       str(user.uuid),
                    'username':   user.username,
                    'email':      user.email,
                    'first_name': user.first_name,
                    'last_name':  user.last_name,
                    'role':       user.role,
                    'is_staff':   user.is_staff,
                    'spaces':     user.get_spaces(),
                },
            })

            sjwt_settings = getattr(settings, 'SIMPLE_JWT', {})
            access_cookie_name = sjwt_settings.get('AUTH_COOKIE', 'access_token')
            refresh_cookie_name = sjwt_settings.get('REFRESH_COOKIE', 'refresh_token')

            samesite_policy = 'None' if not settings.DEBUG else 'Lax'

            response.set_cookie(
                access_cookie_name,
                access_token,
                httponly=True,
                secure=not settings.DEBUG,
                samesite=samesite_policy,
                max_age=60*60*24*7  # 7 jours
            )
            response.set_cookie(
                refresh_cookie_name,
                refresh_token,
                httponly=True,
                secure=not settings.DEBUG,
                samesite=samesite_policy,
                max_age=60*60*24*7
            )
            response.set_cookie(
                'is_logged_in',
                'true',
                httponly=False,
                secure=not settings.DEBUG,
                samesite=samesite_policy,
                max_age=60*60*24*7
            )
            return response
        except ValueError:
            return Response({'error': 'Invalid Google token'}, status=400)


# ────────────────────────────────────────────────
# Auth Mobile (OTP)
# ────────────────────────────────────────────────

def send_otp_email(email, code):
    """
    Envoie le code OTP par email. 
    En production, cette fonction est appelée via un Thread pour ne pas bloquer la réponse API.
    """
    def _send():
        subject = "Votre code de vérification SmartSaha"
        message = f"Votre code de vérification est : {code}\n\nCe code expirera dans 10 minutes."
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            print(f"OTP envoyé avec succès à {email}")
        except Exception as e:
            print(f"Erreur d'envoi d'email à {email} : {e}")

    # Lancement dans un thread séparé pour éviter les timeouts (502)
    email_thread = threading.Thread(target=_send)
    email_thread.start()
    return True

@swagger_auto_schema(tags=['Authentification Mobile'])
class GenerateOTPView(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        operation_summary="Générer un code OTP (Email)",
        tags=['Authentification Mobile'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username'],
            properties={'username': openapi.Schema(type=openapi.TYPE_STRING, description="Nom d'utilisateur")}
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={'message': openapi.Schema(type=openapi.TYPE_STRING)}
            ),
            400: "Données invalides (username manquant ou sans email)",
            404: "Utilisateur non trouvé",
            500: "Échec de l'envoi de l'email"
        }
    )
    def post(self, request):
        username = request.data.get('username')
        if not username:
            return Response({'error': 'username est requis'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Récupération de l'utilisateur pour obtenir son email
        try:
            user = User.objects.get(username=username)
            if not user.email:
                return Response({'error': "Cet utilisateur n'a pas d'adresse email associée."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'Utilisateur introuvable avec ce nom d\'utilisateur.'}, status=status.HTTP_404_NOT_FOUND)

        # Générer un code à 6 chiffres
        code = f"{random.randint(100000, 999999)}"
        
        # Stocker dans le cache pour 5 minutes (300 secondes)
        cache_key = f'otp_{username}'
        cache.set(cache_key, code, timeout=300)
        
        # Envoyer par email
        success = send_otp_email(user.email, code)
        
        if success:
            return Response({'message': f'Code OTP envoyé avec succès à {user.email}.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': "Échec de l'envoi de l'email. Veuillez réessayer plus tard."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@swagger_auto_schema(tags=['Authentification Mobile'])
class VerifyOTPView(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        operation_summary="Vérifier le code OTP",
        tags=['Authentification Mobile'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'code'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description="Nom d'utilisateur"),
                'code': openapi.Schema(type=openapi.TYPE_STRING, description="Code OTP reçu par email")
            }
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING),
                    'user': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id':           openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID),
                            'phone_number': openapi.Schema(type=openapi.TYPE_STRING),
                            'is_phone_verified': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                            'role':         openapi.Schema(type=openapi.TYPE_STRING),
                            'spaces': openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'agriculture':  openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                    'organisation': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                    'superviseur':  openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                }
                            ),
                        }
                    )
                }
            ),
            400: "Code OTP invalide ou expiré",
            404: "Utilisateur non trouvé"
        }
    )
    def post(self, request):
        username = request.data.get('username')
        code = request.data.get('code')
        
        if not username or not code:
            return Response({'error': 'username et code sont requis'}, status=status.HTTP_400_BAD_REQUEST)
        
        cache_key = f'otp_{username}'
        cached_code = cache.get(cache_key)
        
        if not cached_code or str(cached_code) != str(code):
            return Response({'error': 'Code OTP invalide ou expiré'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Le code est bon, on le retire du cache
        cache.delete(cache_key)
        
        # Récupération de l'utilisateur
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'Utilisateur introuvable.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Si on identifie par OTP, on peut considérer qu'au moins l'accès est validé
        # On pourrait aussi vérifier user.is_active ici
        
        if not user.is_phone_verified:
            user.is_phone_verified = True
            user.save()
            
        # Génération des tokens JWT
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        
        response = Response({
            'message': 'Authentification réussie',
            'user': {
                'id': user.uuid,
                'phone_number': user.phone_number,
                'is_phone_verified': user.is_phone_verified,
                'role': user.role,
                'spaces': user.get_spaces(),
            }
        }, status=status.HTTP_200_OK)
        
        # Configuration des cookies HttpOnly
        sjwt_settings = getattr(settings, 'SIMPLE_JWT', {})
        access_cookie_name = sjwt_settings.get('AUTH_COOKIE', 'access_token')
        refresh_cookie_name = sjwt_settings.get('REFRESH_COOKIE', 'refresh_token')
        
        samesite_policy = 'None' if not settings.DEBUG else 'Lax'
        
        response.set_cookie(
            key=access_cookie_name,
            value=access_token,
            httponly=True,
            secure=not settings.DEBUG,
            samesite=samesite_policy,
            max_age=60*60*24*7
        )
        response.set_cookie(
            key=refresh_cookie_name,
            value=refresh_token,
            httponly=True,
            secure=not settings.DEBUG,
            samesite=samesite_policy,
            max_age=60*60*24*7
        )
        # On ajoute également le flag is_logged_in pour la cohérence avec le Web
        response.set_cookie(
            'is_logged_in',
            'true',
            httponly=False,
            secure=not settings.DEBUG,
            samesite=samesite_policy,
            max_age=60*60*24*7
        )
        
        return response


# ────────────────────────────────────────────────
# Inscription Mobile (OTP à l'inscription seulement)
# ────────────────────────────────────────────────

@swagger_auto_schema(tags=['Authentification Mobile'])
class MobileSignupView(APIView):
    """
    Inscription mobile : crée un compte INACTIF et envoie un OTP par email.
    Le compte sera activé après vérification du code via MobileVerifySignupView.
    """
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        operation_summary="Inscription Mobile (création de compte + envoi OTP)",
        tags=['Authentification Mobile'],
        request_body=MobileSignupSerializer,
        responses={
            201: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message':  openapi.Schema(type=openapi.TYPE_STRING),
                    'username': openapi.Schema(type=openapi.TYPE_STRING),
                    'email':    openapi.Schema(type=openapi.TYPE_STRING),
                }
            ),
            400: "Données invalides",
            500: "Échec de l'envoi de l'OTP"
        }
    )
    def post(self, request):
        serializer = MobileSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()  # compte créé avec is_active=False

        # Générer et stocker un code OTP (TTL 10 min)
        code = f"{random.randint(100000, 999999)}"
        cache_key = f'otp_signup_{user.username}'
        cache.set(cache_key, code, timeout=600)

        # Envoyer l'OTP par email (Asynchrone via Threading)
        send_otp_email(user.email, code)

        return Response({
            'message': f'Compte créé. Un code de vérification est en cours d\'envoi à {user.email}.',
            'username': user.username,
            'email':    user.email,
        }, status=status.HTTP_201_CREATED)


@swagger_auto_schema(tags=['Authentification Mobile'])
class MobileVerifySignupView(APIView):
    """
    Vérifie le code OTP d'inscription.
    Si valide : active le compte et retourne les tokens JWT.
    """
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        operation_summary="Vérification OTP d'inscription mobile (activation du compte)",
        tags=['Authentification Mobile'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'code'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'code':     openapi.Schema(type=openapi.TYPE_STRING, description="Code OTP à 6 chiffres"),
            }
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING),
                    'user': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'uuid':       openapi.Schema(type=openapi.TYPE_STRING),
                            'username':   openapi.Schema(type=openapi.TYPE_STRING),
                            'email':      openapi.Schema(type=openapi.TYPE_STRING),
                            'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                            'last_name':  openapi.Schema(type=openapi.TYPE_STRING),
                            'role':       openapi.Schema(type=openapi.TYPE_STRING),
                            'is_staff':   openapi.Schema(type=openapi.TYPE_BOOLEAN),
                            'spaces':     openapi.Schema(type=openapi.TYPE_OBJECT),
                        }
                    )
                }
            ),
            400: "Code OTP invalide ou expiré",
            404: "Utilisateur introuvable"
        }
    )
    def post(self, request):
        username = request.data.get('username')
        code     = request.data.get('code')

        if not username or not code:
            return Response(
                {'error': 'username et code sont requis'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Vérification du code OTP (clé spécifique à l'inscription)
        cache_key   = f'otp_signup_{username}'
        cached_code = cache.get(cache_key)

        if not cached_code or str(cached_code) != str(code):
            return Response(
                {'error': 'Code OTP invalide ou expiré'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Code correct : invalider le cache
        cache.delete(cache_key)

        # Récupérer l'utilisateur (peut être inactif)
        try:
            user = User.objects.get(username=username, is_active=False)
        except User.DoesNotExist:
            return Response(
                {'error': 'Utilisateur introuvable ou déjà activé.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Activer le compte
        user.is_active = True
        user.is_phone_verified = True
        user.save()

        # Générer les tokens JWT
        refresh       = RefreshToken.for_user(user)
        access_token  = str(refresh.access_token)
        refresh_token = str(refresh)

        response = Response({
            'message': 'Compte activé avec succès.',
            'user': {
                'uuid':       str(user.uuid),
                'username':   user.username,
                'email':      user.email,
                'first_name': user.first_name,
                'last_name':  user.last_name,
                'role':       user.role,
                'is_staff':   user.is_staff,
                'spaces':     user.get_spaces(),
            },
        }, status=status.HTTP_200_OK)

        # Poser les cookies HttpOnly (même logique que LoginView)
        sjwt_settings      = getattr(settings, 'SIMPLE_JWT', {})
        access_cookie_name = sjwt_settings.get('AUTH_COOKIE', 'access_token')
        refresh_cookie_name = sjwt_settings.get('REFRESH_COOKIE', 'refresh_token')
        samesite_policy    = 'None' if not settings.DEBUG else 'Lax'

        response.set_cookie(
            access_cookie_name, access_token,
            httponly=True, secure=not settings.DEBUG,
            samesite=samesite_policy, max_age=60*60*24*7
        )
        response.set_cookie(
            refresh_cookie_name, refresh_token,
            httponly=True, secure=not settings.DEBUG,
            samesite=samesite_policy, max_age=60*60*24*7
        )
        response.set_cookie(
            'is_logged_in', 'true',
            httponly=False, secure=not settings.DEBUG,
            samesite=samesite_policy, max_age=60*60*24*7
        )
        return response


# ────────────────────────────────────────────────
# Farmer Directory
# ────────────────────────────────────────────────

@method_decorator(name='list',     decorator=swagger_auto_schema(tags=['Découverte (Discovery)']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(tags=['Découverte (Discovery)']))
class FarmerDirectoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Annuaire de découverte des agriculteurs.
    Retourne uniquement les utilisateurs sans espace organisation
    (ni créateurs d'organisation, ni leaders de groupe).
    """
    serializer_class   = FarmerDirectorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends    = [filters.SearchFilter]
    search_fields      = ['username', 'first_name', 'last_name']

    def get_queryset(self):
        return (
            User.objects
            .filter(is_staff=False)
            # Exclure les créateurs d'organisation
            .exclude(organisations_created__isnull=False)
            # Exclure les leaders actifs de groupe
            .exclude(
                group_memberships__role__role_type='LEADER',
                group_memberships__status='ACTIVE',
            )
            # Exclure l'utilisateur connecté
            .exclude(uuid=self.request.user.uuid)
            .distinct()
        )