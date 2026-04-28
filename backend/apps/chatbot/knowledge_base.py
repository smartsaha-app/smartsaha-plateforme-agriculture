"""
apps/chatbot/knowledge_base.py
-------------------------------
Base de connaissances agricoles Madagascar.
Charge les données locales (calendrier cultural FOFIFA, guides FERT/Ceffel,
données FAOSTAT) et fournit des méthodes de recherche contextuelle.
"""
import json
import os
from typing import Optional

from apps.chatbot.faostat_loader import FAOSTATLoader


class AgriculturalKnowledgeBase:
    """
    Base de connaissances agricoles Madagascar.
    Combine : calendrier cultural FOFIFA + guide bonnes pratiques + FAOSTAT.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._loaded = False
        return cls._instance

    def _ensure_loaded(self):
        if not self._loaded:
            self._load_all()
            self._loaded = True

    def _load_all(self):
        data_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'data',
        )
        self._calendrier = self._load_json(os.path.join(data_dir, 'calendrier_cultural.json'))
        self._guides = self._load_json(os.path.join(data_dir, 'guides_agricoles.json'))
        self._faostat = FAOSTATLoader()
        self._loaded = True
        print("✅ Knowledge Base agricole chargée")

    @staticmethod
    def _load_json(path: str) -> dict:
        if not os.path.exists(path):
            print(f"⚠️ Fichier KB manquant : {path}")
            return {}
        try:
            with open(path, encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Erreur chargement {path} : {e}")
            return {}

    # ── Recherche de culture ──────────────────────────────────────────────────

    def _normalize_crop_name(self, query: str) -> str:
        """Normalise un nom de culture (FR/MG/EN → clé interne)."""
        q = query.lower().strip()

        # Mapping des synonymes courants
        ALIASES = {
            'vary': 'riz', 'rice': 'riz', 'paddy': 'riz',
            'katsaka': 'mais', 'maïs': 'mais', 'corn': 'mais', 'maize': 'mais',
            'tsaramaso': 'haricot', 'bean': 'haricot', 'beans': 'haricot',
            'mangahazo': 'manioc', 'cassava': 'manioc',
            'voanjo': 'arachide', 'peanut': 'arachide', 'groundnut': 'arachide',
            'ampemba': 'sorgho', 'sorghum': 'sorgho',
            'vomanga': 'patate_douce', 'patate douce': 'patate_douce', 'sweet potato': 'patate_douce',
            'lavanila': 'vanille', 'vanilla': 'vanille',
        }

        if q in ALIASES:
            return ALIASES[q]

        # Tentative de correspondance partielle
        for alias, key in ALIASES.items():
            if alias in q or q in alias:
                return key

        # Correspondance directe avec les clés du calendrier
        cultures = self._calendrier.get('cultures', {})
        if q in cultures:
            return q
        for key in cultures:
            if q in key or key in q:
                return key

        return q

    def search_crop_calendar(self, crop_name: str, region: str = None) -> str:
        """
        Cherche le calendrier cultural pour une culture donnée.
        Optionnellement filtré par région.
        """
        self._ensure_loaded()
        key = self._normalize_crop_name(crop_name)
        cultures = self._calendrier.get('cultures', {})
        crop_data = cultures.get(key)

        if not crop_data:
            return ""

        lines = [
            f"## Calendrier Cultural — {crop_name.capitalize()} ({crop_data.get('nom_mg', '')}/{crop_data.get('nom_en', '')})"
        ]

        # Parcourir les zones/types
        zones = crop_data.get('zones', {})
        types = crop_data.get('types', {})
        target = types if types else {'default': {'zones': zones}}

        for type_key, type_data in target.items():
            if types:
                lines.append(f"\n### {type_data.get('label', type_key)}")

            inner_zones = type_data.get('zones', zones)
            for zone_key, zone_info in inner_zones.items():
                if isinstance(zone_info, dict):
                    # Filtrer par région si demandé
                    if region:
                        zone_regions = zone_info.get('regions', [])
                        region_lower = region.lower()
                        if zone_regions and not any(
                            region_lower in r.lower() for r in zone_regions
                        ):
                            continue

                    lines.append(f"\n**Zone : {zone_key.replace('_', ' ').title()}**")
                    if zone_info.get('regions'):
                        lines.append(f"  Régions : {', '.join(zone_info['regions'])}")
                    semis = zone_info.get('semis') or zone_info.get('plantation')
                    if semis:
                        lines.append(f"  Semis/Plantation : {semis['debut']} → {semis['fin']}")
                    recolte = zone_info.get('recolte')
                    if recolte:
                        lines.append(f"  Récolte : {recolte['debut']} → {recolte['fin']}")
                    if zone_info.get('cycle_jours'):
                        c = zone_info['cycle_jours']
                        lines.append(f"  Cycle : {c[0]}-{c[1]} jours")
                    if zone_info.get('varietes_recommandees'):
                        lines.append(f"  Variétés : {', '.join(zone_info['varietes_recommandees'])}")
                    if zone_info.get('rendement_moyen_kg_ha'):
                        lines.append(f"  Rendement moyen : {zone_info['rendement_moyen_kg_ha']:,} kg/ha")

        # Conseils généraux
        conseils = crop_data.get('conseils_generaux', [])
        if conseils:
            lines.append("\n**Conseils :**")
            for c in conseils:
                lines.append(f"  • {c}")

        return '\n'.join(lines) if len(lines) > 1 else ""

    # ── Recherche de pratiques ────────────────────────────────────────────────

    def search_practice(self, topic: str) -> str:
        """
        Cherche dans le guide des bonnes pratiques par sujet.
        Topics : 'sol', 'eau', 'engrais', 'maladie', 'ravageur', 'stockage'
        """
        self._ensure_loaded()
        pratiques = self._guides.get('pratiques_culturales', {})

        TOPIC_MAPPING = {
            'sol': 'preparation_sol',
            'terre': 'preparation_sol',
            'labour': 'preparation_sol',
            'eau': 'gestion_eau',
            'irrigation': 'gestion_eau',
            'arrosage': 'gestion_eau',
            'engrais': 'fertilisation',
            'fumier': 'fertilisation',
            'compost': 'fertilisation',
            'fertilisant': 'fertilisation',
            'maladie': 'protection_cultures',
            'ravageur': 'protection_cultures',
            'insecte': 'protection_cultures',
            'parasite': 'protection_cultures',
            'chenille': 'protection_cultures',
            'puceron': 'protection_cultures',
            'recolte': 'recolte_post_recolte',
            'stockage': 'recolte_post_recolte',
            'conservation': 'recolte_post_recolte',
            'sechage': 'recolte_post_recolte',
            'agroforesterie': 'agroforesterie',
            'arbre': 'agroforesterie',
        }

        topic_lower = topic.lower()
        matched_key = None
        for keyword, key in TOPIC_MAPPING.items():
            if keyword in topic_lower:
                matched_key = key
                break

        if not matched_key:
            return ""

        section = pratiques.get(matched_key, {})
        if not section:
            return ""

        return self._format_practice_section(section, matched_key)

    def _format_practice_section(self, section: dict, key: str) -> str:
        """Formatte une section du guide en texte lisible."""
        lines = [f"## Guide — {section.get('titre_en', key.replace('_', ' ').title())}"]

        if key == 'preparation_sol':
            for etape in section.get('etapes', []):
                lines.append(f"\n**{etape['action']}**")
                lines.append(f"  {etape['description']}")
                if etape.get('quand'):
                    lines.append(f"  Quand : {etape['quand']}")

        elif key == 'gestion_eau':
            for tech in section.get('techniques', []):
                lines.append(f"\n**{tech['nom']}**")
                lines.append(f"  {tech['description']}")
                if tech.get('avantages'):
                    lines.append(f"  Avantage : {tech['avantages']}")

        elif key == 'fertilisation':
            for p in section.get('principes', []):
                lines.append(f"  • {p}")
            for eng in section.get('engrais_organiques', []):
                lines.append(f"\n**{eng['nom']}** — Dose : {eng.get('dose', 'N/A')}")
                if eng.get('application'):
                    lines.append(f"  {eng['application']}")
            for eng in section.get('engrais_mineraux', []):
                lines.append(f"\n**{eng['nom']}** — Usage : {eng['usage']}")
                if eng.get('dose_riz'):
                    lines.append(f"  Dose riz : {eng['dose_riz']}")

        elif key == 'protection_cultures':
            for mal in section.get('maladies_courantes', []):
                lines.append(f"\n**{mal['nom']}**")
                lines.append(f"  Symptômes : {mal['symptomes']}")
                if mal.get('prevention'):
                    lines.append(f"  Prévention : {', '.join(mal['prevention'])}")
            for rav in section.get('ravageurs_courants', []):
                lines.append(f"\n**{rav['nom']}**")
                lines.append(f"  Symptômes : {rav['symptomes']}")
                if rav.get('lutte'):
                    lines.append(f"  Lutte : {', '.join(rav['lutte'])}")

        elif key == 'recolte_post_recolte':
            for p in section.get('principes', []):
                lines.append(f"  • {p}")
            for s in section.get('stockage', []):
                lines.append(f"\n**{s['nom']}** — {s.get('description', s.get('avantage', ''))}")

        return '\n'.join(lines) if len(lines) > 1 else ""

    # ── Recherche combinée ────────────────────────────────────────────────────

    def search(self, query: str, crop_name: str = None, region: str = None) -> str:
        """
        Recherche combinée dans toutes les sources de la KB.
        Retourne le contexte le plus pertinent.
        """
        self._ensure_loaded()
        sections = []

        # 1. Si une culture est mentionnée → calendrier + FAOSTAT
        target_crop = crop_name or self._extract_crop_from_query(query)
        if target_crop:
            cal = self.search_crop_calendar(target_crop, region)
            if cal:
                sections.append(cal)
            fao = self._faostat.format_for_context(target_crop)
            if fao:
                sections.append(fao)

        # 2. Recherche dans les pratiques
        practice = self.search_practice(query)
        if practice:
            sections.append(practice)

        # 3. Rotation et association si pertinent
        if any(kw in query.lower() for kw in ['rotation', 'association', 'après', 'alterner']):
            transversal = self._guides.get('conseils_transversaux', {})
            if transversal.get('rotation_recommandee'):
                sections.append("## Rotation recommandée")
                for r in transversal['rotation_recommandee']:
                    sections.append(f"  • {r}")
            if transversal.get('association_cultures'):
                sections.append("\n## Associations de cultures")
                for a in transversal['association_cultures']:
                    sections.append(f"  • {a['association']} — {a['avantage']}")

        # 4. Saisons si pertinent
        if any(kw in query.lower() for kw in ['saison', 'quand', 'mois', 'période', 'asara', 'ririnina']):
            saisons = self._calendrier.get('saisons_madagascar', {})
            if saisons:
                sections.append("\n## Saisons agricoles Madagascar")
                for s_key, s_data in saisons.items():
                    sections.append(
                        f"  • **{s_data['label']}** ({', '.join(s_data['mois'])}) : {s_data['description']}"
                    )

        return '\n\n'.join(sections)

    def _extract_crop_from_query(self, query: str) -> Optional[str]:
        """Détecte automatiquement une culture mentionnée dans la question."""
        q = query.lower()
        CROP_KEYWORDS = {
            'riz': ['riz', 'vary', 'rice', 'paddy', 'rizière', 'tanimbary'],
            'mais': ['maïs', 'mais', 'katsaka', 'corn', 'maize'],
            'haricot': ['haricot', 'tsaramaso', 'bean'],
            'manioc': ['manioc', 'mangahazo', 'cassava'],
            'arachide': ['arachide', 'voanjo', 'peanut', 'groundnut'],
            'sorgho': ['sorgho', 'ampemba', 'sorghum'],
            'patate_douce': ['patate douce', 'vomanga', 'sweet potato'],
            'vanille': ['vanille', 'lavanila', 'vanilla'],
            'tomate': ['tomate', 'tomato'],
            'oignon': ['oignon', 'tongolo', 'onion'],
            'pomme de terre': ['pomme de terre', 'potato', 'ovy'],
            'café': ['café', 'coffee', 'kafe'],
            'cacao': ['cacao', 'cocoa'],
            'girofle': ['girofle', 'clou de girofle', 'clove'],
            'poivre': ['poivre', 'pepper', 'dipoavatra'],
        }

        for crop_key, keywords in CROP_KEYWORDS.items():
            for kw in keywords:
                if kw in q:
                    return crop_key
        return None

    def get_seasons_info(self) -> str:
        """Retourne les informations sur les saisons agricoles de Madagascar."""
        self._ensure_loaded()
        saisons = self._calendrier.get('saisons_madagascar', {})
        if not saisons:
            return ""
        lines = ["## Saisons agricoles Madagascar"]
        for s_data in saisons.values():
            lines.append(f"  • **{s_data['label']}** ({', '.join(s_data['mois'])}): {s_data['description']}")
        return '\n'.join(lines)
