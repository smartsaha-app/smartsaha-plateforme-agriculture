"""
apps/chatbot/context_builder.py
--------------------------------
Construit le contexte RAG enrichi pour les assistants IA.
Intègre : données parcelle + historique chat + base de connaissances +
alertes actives + tâches en cours.

v2.0 — Contexte structuré en sections Markdown pour une meilleure
       exploitation par le LLM.
"""
from typing import Optional


class ContextBuilder:
    """
    Construit un contexte complet et structuré pour l'assistant agronome.
    Le contexte est organisé en sections claires pour que le LLM puisse
    exploiter efficacement les données.
    """

    @staticmethod
    def build_context(
        parcel_uuid: str = None,
        user_modules: dict = None,
        chat_history: list = None,
        knowledge_query: str = None,
        crop_name: str = None,
        user=None,
    ) -> str:
        """
        Construit le contexte complet pour l'assistant agronome.

        Args:
            parcel_uuid: UUID de la parcelle sélectionnée
            user_modules: dict de modules activés (parcel, soil, weather, crops, yield_records)
            chat_history: liste des messages précédents [{'role': ..., 'content': ...}]
            knowledge_query: requête pour la base de connaissances
            crop_name: nom de la culture (pour recherche KB ciblée)
            user: instance User Django (pour les alertes et tâches)
        """
        from apps.parcels.models import Parcel

        user_modules = user_modules or {}
        sections = []

        # ── 1. Historique de conversation ─────────────────────────────────────
        if chat_history:
            history_section = ContextBuilder._build_history_section(chat_history)
            if history_section:
                sections.append(history_section)

        # ── 2. Données parcelle ───────────────────────────────────────────────
        parcel = None
        if parcel_uuid:
            try:
                parcel = Parcel.objects.get(uuid=parcel_uuid)
            except Parcel.DoesNotExist:
                sections.append("⚠️ Parcelle inconnue (UUID introuvable)")

        if parcel:
            parcel_section = ContextBuilder._build_parcel_section(parcel, user_modules)
            if parcel_section:
                sections.append(parcel_section)

        # ── 3. Base de connaissances agricoles ────────────────────────────────
        if knowledge_query or crop_name:
            kb_section = ContextBuilder._build_knowledge_section(
                knowledge_query or '', crop_name
            )
            if kb_section:
                sections.append(kb_section)

        # ── 4. Alertes actives ────────────────────────────────────────────────
        if parcel:
            alerts_section = ContextBuilder._build_alerts_section(parcel)
            if alerts_section:
                sections.append(alerts_section)

        # ── 5. Tâches en cours ────────────────────────────────────────────────
        if parcel:
            tasks_section = ContextBuilder._build_tasks_section(parcel)
            if tasks_section:
                sections.append(tasks_section)

        return '\n\n'.join(sections)

    # ── Sections individuelles ────────────────────────────────────────────────

    @staticmethod
    def _build_history_section(chat_history: list) -> str:
        """Formatte l'historique de conversation pour le prompt."""
        if not chat_history:
            return ""

        lines = ["## Historique de conversation récent"]
        for msg in chat_history[-8:]:  # Max 8 derniers messages
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            # Tronquer les messages longs
            if len(content) > 300:
                content = content[:300] + '…'
            prefix = '👤' if role == 'user' else '🤖'
            lines.append(f"{prefix} **{role.capitalize()}** : {content}")

        return '\n'.join(lines)

    @staticmethod
    def _build_parcel_section(parcel, user_modules: dict) -> str:
        """Construit la section données parcelle de manière structurée."""
        from apps.dashboard.services import ParcelDataService

        lines = ["## Données de la Parcelle"]

        if user_modules.get('parcel', False):
            lines.append(f"**Nom** : {parcel.parcel_name}")
            center = parcel.get_center()
            if center:
                lines.append(f"**Coordonnées** : {center['lat']:.4f}, {center['lng']:.4f}")

        if user_modules.get('soil', False):
            try:
                soil_info = ParcelDataService.fetch_soil(parcel)
                if soil_info and soil_info.data:
                    lines.append("\n### Données Sol (ISRIC SoilGrids)")
                    layers = soil_info.data.get('properties', {}).get('layers', [])
                    for layer in layers:
                        name = layer.get('name', '')
                        unit = layer.get('unit_measure', {}).get('target_units', '')
                        for depth in layer.get('depths', []):
                            val = depth.get('values', {}).get('mean')
                            if val is not None:
                                lines.append(f"  - {name} : {val} {unit}")
            except Exception as e:
                lines.append(f"  ⚠️ Sol : données indisponibles ({e})")

        if user_modules.get('weather', False):
            try:
                weather_info = ParcelDataService.fetch_weather(parcel)
                if weather_info:
                    lines.append("\n### Données Météo")
                    lines.append(f"  - Température : {weather_info.current_temperature}°C")
                    lines.append(f"  - Précipitations : {weather_info.total_precipitation} mm")
                    lines.append(f"  - Niveau de risque : {weather_info.risk_level}")
                    lines.append(f"  - Lieu : {weather_info.location_name}")
                    summary = weather_info.get_weather_summary()
                    if summary:
                        lines.append(f"  - Résumé : {summary}")
            except Exception as e:
                lines.append(f"  ⚠️ Météo : données indisponibles ({e})")

        if user_modules.get('crops', False):
            try:
                crops_info = ParcelDataService.build_parcel_crops(parcel)
                if crops_info:
                    lines.append("\n### Cultures en cours")
                    for crop in crops_info:
                        if isinstance(crop, dict):
                            lines.append(f"  - {crop.get('crop_name', 'N/A')} (planté le {crop.get('planting_date', '?')})")
                            if crop.get('tasks'):
                                for task in crop['tasks'][:3]:
                                    status = task.get('status', '?')
                                    lines.append(f"    • {task.get('name', '?')} [{status}]")
                        else:
                            lines.append(f"  - {crop}")
            except Exception as e:
                lines.append(f"  ⚠️ Cultures : données indisponibles ({e})")

        if user_modules.get('yield_records', False):
            try:
                yields_info = ParcelDataService.build_yield_records(parcel)
                if yields_info:
                    lines.append("\n### Historique Rendements")
                    if isinstance(yields_info, list):
                        for y in yields_info[:5]:
                            if isinstance(y, dict):
                                lines.append(
                                    f"  - {y.get('crop_name', '?')} : "
                                    f"{y.get('yield_amount', '?')} {y.get('unit', 'kg')}"
                                )
                            else:
                                lines.append(f"  - {y}")
                    else:
                        lines.append(f"  {yields_info}")
            except Exception as e:
                lines.append(f"  ⚠️ Rendements : données indisponibles ({e})")

        return '\n'.join(lines) if len(lines) > 1 else ""

    @staticmethod
    def _build_knowledge_section(query: str, crop_name: str = None) -> str:
        """Interroge la base de connaissances agricoles."""
        try:
            from apps.chatbot.knowledge_base import AgriculturalKnowledgeBase
            kb = AgriculturalKnowledgeBase()
            result = kb.search(query, crop_name=crop_name)
            if result:
                return f"## Base de Connaissances Agricoles Madagascar\n{result}"
        except Exception as e:
            print(f"⚠️ Knowledge Base error: {e}")
        return ""

    @staticmethod
    def _build_alerts_section(parcel) -> str:
        """Récupère les alertes actives pour la parcelle."""
        try:
            from apps.weather.models import WeatherData
            latest = WeatherData.objects.filter(
                parcel=parcel
            ).order_by('-created_at').first()

            if not latest:
                return ""

            alerts = latest.agricultural_alerts
            high_alerts = [a for a in alerts if a.get('severity') in ('HIGH', 'CRITICAL')]

            if not high_alerts:
                return ""

            lines = ["## ⚠️ Alertes Actives"]
            for alert in high_alerts[:5]:
                lines.append(
                    f"  - [{alert['severity']}] {alert['type']} : {alert['message']}"
                )
                if alert.get('action'):
                    lines.append(f"    Action recommandée : {alert['action']}")

            return '\n'.join(lines)
        except Exception:
            return ""

    @staticmethod
    def _build_tasks_section(parcel) -> str:
        """Récupère les tâches urgentes ou en retard."""
        try:
            from apps.tasks.models import Task
            from django.utils import timezone
            import datetime

            today = timezone.now().date()
            overdue = Task.objects.filter(
                parcelCrop__parcel=parcel,
                completed_at__isnull=True,
                due_date__lt=today,
            ).order_by('due_date')[:5]

            upcoming = Task.objects.filter(
                parcelCrop__parcel=parcel,
                completed_at__isnull=True,
                due_date__gte=today,
                due_date__lte=today + datetime.timedelta(days=7),
            ).order_by('due_date')[:3]

            if not overdue and not upcoming:
                return ""

            lines = ["## 📋 Tâches"]
            if overdue:
                lines.append("**En retard :**")
                for t in overdue:
                    lines.append(f"  - ⏰ {t.name} (échéance : {t.due_date})")
            if upcoming:
                lines.append("**À venir (7 jours) :**")
                for t in upcoming:
                    lines.append(f"  - 📌 {t.name} (échéance : {t.due_date})")

            return '\n'.join(lines)
        except Exception:
            return ""