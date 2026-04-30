"""
apps/chatbot/faostat_loader.py
-------------------------------
Charge et indexe les données FAOSTAT Madagascar pour le RAG.
Source : data/FAOSTAT_data_fr_9-11-2025.csv
"""
import csv
import os
from functools import lru_cache
from typing import Optional


class FAOSTATLoader:
    """
    Charge les données FAOSTAT Madagascar (production, rendement, superficie)
    et fournit des méthodes de recherche pour enrichir le contexte du chatbot.
    """

    _instance = None
    _data: list = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._loaded = False
        return cls._instance

    def _ensure_loaded(self):
        if not self._loaded:
            self._load_data()
            self._loaded = True

    def _load_data(self):
        """Charge le CSV FAOSTAT au premier accès."""
        csv_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'data', 'FAOSTAT_data_fr_9-11-2025.csv',
        )
        if not os.path.exists(csv_path):
            print(f"⚠️ FAOSTAT CSV introuvable : {csv_path}")
            return

        try:
            with open(csv_path, encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self._data = list(reader)
            print(f"✅ FAOSTAT : {len(self._data)} enregistrements chargés")
        except Exception as e:
            print(f"❌ Erreur chargement FAOSTAT : {e}")

    # ── Recherche par culture ─────────────────────────────────────────────────

    def search_by_crop(self, crop_name: str) -> dict:
        """
        Recherche les données FAOSTAT pour une culture donnée.
        Retourne rendement, superficie et production.
        """
        self._ensure_loaded()
        crop_lower = crop_name.lower().strip()

        results = {
            'culture': crop_name,
            'production': None,
            'rendement': None,
            'superficie': None,
            'source': 'FAOSTAT 2023 - Madagascar',
        }

        for row in self._data:
            produit = row.get('Produit', '').lower()
            if crop_lower not in produit:
                continue

            element = row.get('Élément', '')
            valeur = row.get('Valeur', '')
            unite = row.get('Unité', '')

            if not valeur:
                continue

            try:
                val = float(valeur.replace(',', ''))
            except ValueError:
                continue

            if 'Production' in element:
                results['production'] = {'valeur': val, 'unite': unite}
            elif 'Rendement' in element:
                results['rendement'] = {'valeur': val, 'unite': unite}
            elif 'Superficie' in element:
                results['superficie'] = {'valeur': val, 'unite': unite}

        return results

    def get_top_crops(self, n: int = 10) -> list:
        """Retourne les top N cultures par production à Madagascar."""
        self._ensure_loaded()

        productions = {}
        for row in self._data:
            if row.get('Élément', '') != 'Production':
                continue
            unite = row.get('Unité', '')
            if unite != 'tonnes':
                continue
            produit = row.get('Produit', '')
            valeur = row.get('Valeur', '')
            if not valeur:
                continue
            try:
                productions[produit] = float(valeur.replace(',', ''))
            except ValueError:
                pass

        sorted_crops = sorted(productions.items(), key=lambda x: x[1], reverse=True)
        return [
            {'culture': name, 'production_tonnes': val}
            for name, val in sorted_crops[:n]
        ]

    def compare_yield(self, crop_name: str, user_yield_kg_ha: float) -> str:
        """Compare le rendement de l'agriculteur avec la moyenne nationale FAOSTAT."""
        data = self.search_by_crop(crop_name)
        national = data.get('rendement')
        if not national:
            return f"Données de rendement national non disponibles pour '{crop_name}'."

        national_val = national['valeur']
        diff_pct = ((user_yield_kg_ha - national_val) / national_val) * 100

        if diff_pct > 10:
            emoji = '🌟'
            evaluation = 'supérieur'
        elif diff_pct > -10:
            emoji = '✅'
            evaluation = 'dans la moyenne'
        else:
            emoji = '⚠️'
            evaluation = 'inférieur'

        return (
            f"{emoji} Votre rendement de {user_yield_kg_ha:,.0f} kg/ha est {evaluation} "
            f"à la moyenne nationale de {national_val:,.1f} {national['unite']} "
            f"({diff_pct:+.0f}%). Source : FAOSTAT 2023."
        )

    def format_for_context(self, crop_name: str) -> str:
        """Formatte les données FAOSTAT pour injection dans le prompt."""
        data = self.search_by_crop(crop_name)

        lines = [f"## Données Nationales FAOSTAT 2023 — {crop_name}"]
        if data['production']:
            lines.append(f"- Production nationale : {data['production']['valeur']:,.0f} {data['production']['unite']}")
        if data['rendement']:
            lines.append(f"- Rendement moyen national : {data['rendement']['valeur']:,.1f} {data['rendement']['unite']}")
        if data['superficie']:
            lines.append(f"- Superficie cultivée : {data['superficie']['valeur']:,.0f} {data['superficie']['unite']}")

        if len(lines) == 1:
            return ""
        return '\n'.join(lines)

    def format_top_crops_for_context(self, n: int = 5) -> str:
        """Formatte les top cultures pour injection dans le prompt."""
        top = self.get_top_crops(n)
        if not top:
            return ""
        lines = ["## Top cultures Madagascar (Production FAOSTAT 2023)"]
        for i, item in enumerate(top, 1):
            lines.append(f"  {i}. {item['culture']} : {item['production_tonnes']:,.0f} tonnes")
        return '\n'.join(lines)
