"""
Settings de base — communs à tous les environnements.
Ne jamais mettre de valeurs sensibles ici (mots de passe, clés API).
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Chemin racine du projet (dossier backend/)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ── APPLICATIONS ──────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Apps internes
    'apps.core',
    'apps.users',
    'apps.parcels',
    'apps.crops',
    'apps.tasks',
    'apps.yields',
    'apps.groups',
    'apps.weather',
    'apps.chatbot',
    'apps.dashboard',
    'suivi_evaluation',

    # Packages tiers
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'drf_yasg',
    'corsheaders',
    'django_filters',
    
    # Nouvelles Apps (Multi-platform)
    'apps.kyc',
    'apps.marketplace',
    'apps.messaging',
    'apps.payments',
]

# ── CORS ──────────────────────────────────────────────
CORS_ALLOW_CREDENTIALS = True

# ── MIDDLEWARE ────────────────────────────────────────
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',       # CORS en premier obligatoirement
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',   # Juste après Security pour les statics
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ── URLS & WSGI ───────────────────────────────────────
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

# ── TEMPLATES ─────────────────────────────────────────
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ── AUTH ──────────────────────────────────────────────
AUTH_USER_MODEL = 'users.User'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ── DRF ───────────────────────────────────────────────
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'apps.core.authentication.CookieJWTAuthentication',
        'apps.core.authentication.CookieTokenAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# ── INTERNATIONALISATION ──────────────────────────────
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Indian/Antananarivo'
USE_I18N = True
USE_TZ = True

# ── DIVERS ────────────────────────────────────────────
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ── SIMPLE JWT SECURE COOKIES ─────────────────────────
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'AUTH_COOKIE': 'access_token',
    'REFRESH_COOKIE': 'refresh_token',
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'USER_ID_FIELD': 'uuid',
}

# ── CACHE ─────────────────────────────────────────────
# En local : LocMemCache (rapide, sans dépendance externe)
# En production : Remplacer par django-redis (voir settings/production.py)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'smartsaha-local-cache',
    }
}

# Durées de cache par type de données (en secondes)
CACHE_TTL_DASHBOARD  = 60 * 5   # 5 minutes  — Dashboards dynamiques (BI, Admin)
CACHE_TTL_STATIC     = 60 * 30  # 30 minutes — Données peu changeantes (cultures, types)
CACHE_TTL_WEATHER    = 60 * 10  # 10 minutes — Données météo (API externe)


# ── STATIC FILES ──────────────────────────────────────
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ── MEDIA FILES ───────────────────────────────────────
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Whitenoise : compression + cache busting automatique
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# ── CLÉS API (lues depuis .env) ───────────────────────
WEATHER_API_KEY    = os.getenv('WEATHER_API_KEY')
GEMINI_API_KEY     = os.getenv('GEMINI_API_KEY')
MISTRAL_API_KEY    = os.getenv('MISTRAL_API_KEY')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')

# Payments API Keys
MVOLA_CONSUMER_KEY = os.getenv('MVOLA_CONSUMER_KEY')
MVOLA_CONSUMER_SECRET = os.getenv('MVOLA_CONSUMER_SECRET')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
ORANGE_MONEY_CLIENT_ID = os.getenv('ORANGE_MONEY_CLIENT_ID')
FIREBASE_SERVER_KEY = os.getenv('FIREBASE_SERVER_KEY')

# ── EMAIL (configuration commune) ─────────────────────
EMAIL_HOST          = os.getenv('EMAIL_HOST')
EMAIL_PORT          = int(os.getenv('EMAIL_PORT'))
EMAIL_USE_TLS       = True
EMAIL_HOST_USER     = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL  = EMAIL_HOST_USER
EMAIL_TIMEOUT       = 10
