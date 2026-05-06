from django.conf import settings
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import exceptions
try:
    from drf_spectacular.extensions import OpenApiAuthenticationExtension
except ImportError:
    OpenApiAuthenticationExtension = None

class CookieJWTAuthentication(JWTAuthentication):
    """
    Classe d'authentification personnalisée qui tente de lire le jeton JWT
    depuis un cookie si l'en-tête Authorization est manquant.
    """
    def authenticate(self, request):
        header = self.get_header(request)
        
        if header is None:
            # Tenter de récupérer le token depuis le cookie
            sjwt_settings = getattr(settings, 'SIMPLE_JWT', {})
            cookie_name = sjwt_settings.get('AUTH_COOKIE', 'access_token')
            raw_token = request.COOKIES.get(cookie_name)
            
            try:
                validated_token = self.get_validated_token(raw_token)
                return self.get_user(validated_token), validated_token
            except exceptions.AuthenticationFailed:
                return None

        # Fallback sur le comportement standard (header)
        return super().authenticate(request)


class CookieTokenAuthentication(TokenAuthentication):
    """
    Classe d'authentification personnalisée qui tente de lire le jeton DRF
    depuis un cookie si l'en-tête Authorization est manquant.
    """
    def authenticate(self, request):
        # 1. Tenter l'authentification standard (En-tête Authorization)
        auth = super().authenticate(request)
        if auth is not None:
            return auth

        # 2. Si non trouvé, tenter de lire le cookie 'auth_token'
        token_key = request.COOKIES.get('auth_token')
        if not token_key:
            return None

        return self.authenticate_credentials(token_key)

# Extensions pour drf-spectacular documentation
if OpenApiAuthenticationExtension:
    class CookieJWTScheme(OpenApiAuthenticationExtension):
        target_class = 'apps.core.authentication.CookieJWTAuthentication'
        name = 'cookieJWT'

        def get_security_definition(self, auto_schema):
            return {
                'type': 'apiKey',
                'in': 'cookie',
                'name': 'access_token',
            }

    class CookieTokenScheme(OpenApiAuthenticationExtension):
        target_class = 'apps.core.authentication.CookieTokenAuthentication'
        name = 'cookieToken'

        def get_security_definition(self, auto_schema):
            return {
                'type': 'apiKey',
                'in': 'cookie',
                'name': 'auth_token',
            }
