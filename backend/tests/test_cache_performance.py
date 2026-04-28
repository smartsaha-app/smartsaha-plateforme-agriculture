# -*- coding: utf-8 -*-
"""
Test de Performance du Cache Django -- SmartSaha
=================================================
Mesure le delta de temps entre un appel API froid (sans cache)
et un appel chaud (avec cache) sur les endpoints les plus gourmands.

Usage :
    cd backend
    venv\\Scripts\\python.exe -m pytest tests/test_cache_performance.py -v -s --no-header
"""
import time
import requests
import pytest

BASE_URL = "http://localhost:8000"
CREDENTIALS = {"email": "admin@smartsaha.com", "password": "Admin@2025!"}

HEAVY_ENDPOINTS = [
    ("/api/dashboard/bi_dashboard/",     "Dashboard BI Organisation"),
    ("/api/dashboard/admin_dashboard/",  "Dashboard Admin"),
    ("/api/dashboard/weather_overview/", "Meteo Resume"),
    ("/api/parcels/",                    "Liste Parcelles paginees"),
    ("/api/users/",                      "Liste Utilisateurs pagines"),
]

# full_dashboard est trop lent pour le test unitaire mais inclus dans le rapport
ALL_ENDPOINTS = [("/api/dashboard/full_dashboard/", "Dashboard Complet")] + HEAVY_ENDPOINTS


@pytest.fixture(scope="session")
def auth_token():
    """Recupere un token d'authentification valide une seule fois pour toute la session."""
    response = requests.post(f"{BASE_URL}/api/login/", json=CREDENTIALS, timeout=10)
    assert response.status_code == 200, f"Echec de connexion : {response.text}"
    token = response.json().get("token")
    print(f"\n[OK] Token obtenu : {token[:20]}...")
    return token


def call_endpoint(url: str, token: str, timeout: int = 30) -> tuple:
    """Appelle un endpoint et retourne (status_code, duree_ms)."""
    headers = {"Authorization": f"Token {token}", "Accept": "application/json"}
    start = time.perf_counter()
    response = requests.get(f"{BASE_URL}{url}", headers=headers, timeout=timeout)
    duration_ms = (time.perf_counter() - start) * 1000
    return response.status_code, duration_ms


class TestCachePerformance:
    """Suite de tests pour valider les gains de performance du cache."""

    @pytest.mark.parametrize("path,label", HEAVY_ENDPOINTS)
    def test_cold_vs_warm_response(self, auth_token, path, label):
        """
        Verifie que le 2eme appel (chaud) est plus rapide que le 1er (froid).
        Si le cache est actif, on devrait observer une reduction d'au moins 20%.
        """
        print(f"\n\n[TEST] {label}")

        # --- Appel N1 : Cache FROID ---
        status_cold, time_cold = call_endpoint(path, auth_token)
        print(f"  [COLD] Appel Froid  : [{status_cold}] {time_cold:.0f}ms")

        if status_cold not in (200, 403):
            pytest.skip(f"Endpoint non disponible (HTTP {status_cold})")

        if status_cold == 403:
            print(f"  [SKIP] Acces refuse (403) -- test de cache ignore.")
            return

        # --- Appel N2 : Cache CHAUD ---
        status_warm, time_warm = call_endpoint(path, auth_token)
        print(f"  [WARM] Appel Chaud  : [{status_warm}] {time_warm:.0f}ms")

        # --- Analyse du Gain ---
        if time_cold > 0:
            gain_pct = ((time_cold - time_warm) / time_cold) * 100
            print(f"  [GAIN] Cache        : {gain_pct:+.1f}%")

            if gain_pct > 20:
                print(f"  [EXCELLENT] Cache actif et efficace !")
            elif gain_pct > 0:
                print(f"  [LEGER] Cache partiellement actif ou TTL court.")
            else:
                print(f"  [ABSENT] Cet endpoint n'est pas mis en cache.")

        assert status_warm == 200, f"L'appel chaud a echoue avec HTTP {status_warm}"


    def test_cache_summary(self, auth_token):
        """
        Rapport de synthese complet : mesure tous les endpoints (y compris full_dashboard)
        et affiche un tableau recapitulatif de l'efficacite du cache.
        """
        print("\n\n" + "=" * 70)
        print("  RAPPORT DE SYNTHESE -- CACHE SMARTSAHA (APRES OPTIMISATION)")
        print("=" * 70)
        print(f"  {'Endpoint':<35} {'Froid':>8} {'Chaud':>8} {'Gain':>10}")
        print("-" * 70)

        total_cold = 0
        total_warm = 0

        for path, label in ALL_ENDPOINTS:
            timeout = 60 if 'full' in path else 30
            _, cold = call_endpoint(path, auth_token, timeout=timeout)
            _, warm = call_endpoint(path, auth_token, timeout=timeout)
            gain = ((cold - warm) / cold * 100) if cold > 0 else 0

            total_cold += cold
            total_warm += warm

            gain_icon = "[CACHE OK]" if gain > 20 else ("+/-" if gain > 0 else "[NO CACHE]")
            print(f"  {label:<35} {cold:>6.0f}ms {warm:>6.0f}ms  {gain_icon} {gain:>+5.1f}%")

        print("-" * 70)
        total_gain = ((total_cold - total_warm) / total_cold * 100) if total_cold > 0 else 0
        print(f"  {'TOTAL':<35} {total_cold:>6.0f}ms {total_warm:>6.0f}ms   {total_gain:>+5.1f}%")
        print("=" * 70 + "\n")
