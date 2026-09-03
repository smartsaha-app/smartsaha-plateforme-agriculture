import requests

from django.conf import settings


class FlaskFAO56Error(Exception):
    """Erreur lors de la communication avec le service Flask FAO56."""
    pass


def _post(endpoint: str, payload: dict) -> dict:
    """
    Envoie une requête POST au service Flask FAO56.
    """

    url = f"{settings.FLASK_SERVICE_URL.rstrip('/')}/{endpoint.lstrip('/')}"

    headers = {
        "X-API-Key": settings.FLASK_SERVICE_API_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    try:
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=60,
        )

    except requests.RequestException as exc:
        raise FlaskFAO56Error(
            "Impossible de contacter le service Flask FAO56."
        ) from exc

    if not response.ok:
        try:
            error_data = response.json()
        except ValueError:
            error_data = {}

        message = error_data.get(
            "message",
            f"Le service Flask a retourné HTTP {response.status_code}."
        )

        raise FlaskFAO56Error(message)

    try:
        return response.json()
    except ValueError as exc:
        raise FlaskFAO56Error(
            "Le service Flask a retourné une réponse JSON invalide."
        ) from exc


def fao56_tree(
    crop: str,
    lat: float,
    long: float,
    irrigation: dict | None = None,
) -> dict:
    """
    Appelle /fao_56_tree.
    """

    payload = {
        "crop": crop,
        "lat": lat,
        "long": long,
    }

    if irrigation is not None:
        payload["irrigation"] = irrigation

    return _post("/fao_56_tree", payload)


def fao56_other(
    crop: str,
    lat: float,
    long: float,
    start_date: str,
    irrigation: dict | None = None,
) -> dict:
    """
    Appelle /fao_56_other.
    """

    payload = {
        "crop": crop,
        "lat": lat,
        "long": long,
        "start_date": start_date,
    }

    if irrigation is not None:
        payload["irrigation"] = irrigation

    return _post("/fao_56_other", payload)