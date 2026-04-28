"""
apps/core/exceptions.py
-----------------------
Exceptions métier partagées par toutes les apps.
Toutes héritent de rest_framework.exceptions pour
être automatiquement sérialisées par DRF.
"""
from rest_framework import status
from rest_framework.exceptions import APIException


class SmartSahaException(APIException):
    """Exception de base pour toutes les erreurs métier SmartSaha."""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Une erreur est survenue."
    default_code = "smartsaha_error"


class ResourceNotFoundException(SmartSahaException):
    """La ressource demandée n'existe pas."""
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Ressource introuvable."
    default_code = "not_found"


class PermissionDeniedException(SmartSahaException):
    """L'utilisateur n'a pas les droits nécessaires."""
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "Vous n'avez pas les droits pour cette action."
    default_code = "permission_denied"


class InvalidStateException(SmartSahaException):
    """L'objet est dans un état invalide pour cette opération."""
    status_code = status.HTTP_409_CONFLICT
    default_detail = "L'état de l'objet ne permet pas cette action."
    default_code = "invalid_state"


class ExternalServiceException(SmartSahaException):
    """Erreur lors d'un appel à une API externe (WeatherAPI, Gemini…)."""
    status_code = status.HTTP_502_BAD_GATEWAY
    default_detail = "Le service externe est temporairement indisponible."
    default_code = "external_service_error"