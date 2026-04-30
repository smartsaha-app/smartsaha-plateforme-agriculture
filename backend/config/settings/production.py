import os
from .base import *

# Empêcher Matplotlib de bloquer le démarrage en construisant son cache
os.environ['MPLCONFIGDIR'] = '/tmp/matplotlib_cache'

EMAIL_BACKEND = 'apps.core.email_backends.ResendEmailBackend'

DEBUG = False
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-dev-key-change-in-production')

ALLOWED_HOSTS = [
    origin.strip()
    for origin in os.getenv('ALLOWED_HOSTS', '').split(',')
    if origin.strip()
]

# Render gère SSL en amont — ne pas rediriger côté Django
SECURE_SSL_REDIRECT = False
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE        = True
CSRF_COOKIE_SECURE           = True
SESSION_COOKIE_SAMESITE      = 'None'
CSRF_COOKIE_SAMESITE         = 'None'
SECURE_HSTS_SECONDS          = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD          = True

# ── BASE DE DONNÉES ───────────────────────────────────
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# ── CACHE (Redis ou Database) ───────────────────────────
REDIS_URL = os.getenv('REDIS_URL')
if REDIS_URL:
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': REDIS_URL,
            'TIMEOUT': 3600,
            'OPTIONS': {'CLIENT_CLASS': 'django_redis.client.DefaultClient'},
        }
    }
    SESSION_ENGINE      = 'django.contrib.sessions.backends.cache'
    SESSION_CACHE_ALIAS = 'default'
else:
    # Fallback sur la base de données (nécessite: python manage.py createcachetable)
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
            'LOCATION': 'django_cache',
        }
    }
    SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# ── CORS ─────────────────────────────────────────────
CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv('CORS_ALLOWED_ORIGINS', '').split(',')
    if origin.strip()
]

# ── STATIC FILES ──────────────────────────────────────
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL  = '/static/'

# ── MEDIA FILES (CLOUDINARY) ──────────────────────────
INSTALLED_APPS += ['cloudinary', 'cloudinary_storage']

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
}

STORAGES['default'] = {
    'BACKEND': 'cloudinary_storage.storage.MediaCloudinaryStorage',
}