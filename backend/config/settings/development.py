"""
Settings de développement local.
Utilisé quand DJANGO_SETTINGS_MODULE=config.settings.development
"""
from .base import *  # noqa: F401, F403

# ── SÉCURITÉ ─────────────────────────────────────────
DEBUG = True
SECRET_KEY = os.getenv(
    'SECRET_KEY',
    'django-insecure-dev-key-change-in-production-000000000'
)
ALLOWED_HOSTS = [
    origin.strip()
    for origin in os.getenv('ALLOWED_HOSTS', '').split(',')
    if origin.strip()
]

# ── BASE DE DONNÉES ───────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME':     os.getenv('DATABASE_NAME'),
        'USER':     os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST':     os.getenv('DATABASE_HOST'),
        'PORT':     os.getenv('DATABASE_PORT'),
    }
}

# ── CACHE (En local : DatabaseCache pour partage entre processus runserver/pytest) ──
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'smartsaha_cache_table',
    }
}
SESSION_ENGINE     = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# ── CORS ─────────────────────────────────────────────
CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv('CORS_ALLOWED_ORIGINS', '').split(',')
    if origin.strip()
]

# ── EMAIL (Activation du SMTP en dev pour test) ──
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# ── CELERY ───────────────────────────────────────────
from celery.schedules import crontab
CELERY_BEAT_SCHEDULE = {
    'collect-weather-data-daily': {
        'task': 'apps.weather.tasks.collect_weather_data',
        'schedule': crontab(hour=6, minute=0),
    },
}