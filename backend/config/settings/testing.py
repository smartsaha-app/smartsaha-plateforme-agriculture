"""
Settings pour les tests automatisés.
Utilisé quand DJANGO_SETTINGS_MODULE=config.settings.testing
"""
from .base import *  # noqa: F401, F403

DEBUG = False
SECRET_KEY = os.getenv(
    'SECRET_KEY',
    'django-insecure-dev-key-change-in-production-000000000'
)
ALLOWED_HOSTS = [
    origin.strip()
    for origin in os.getenv('ALLOWED_HOSTS', '').split(',')
    if origin.strip()
]

# SQLite en mémoire → tests ultra-rapides, pas de vraie BDD
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Cache factice → pas de Redis nécessaire pour les tests
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Email → pas d'envoi réel pendant les tests
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Désactiver la compression des mots de passe → tests plus rapides
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]