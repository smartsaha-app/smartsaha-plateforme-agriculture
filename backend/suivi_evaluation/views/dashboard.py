"""
suivi_evaluation/views/dashboard.py
-------------------------------------
Dashboard S&E scopé par organisation.
L'organisation est résolue depuis request.user → MemberGroup → Group → Organisation.
Chaque utilisateur ne voit que les données de SON organisation.
"""
from django.db.models import Avg, Sum, Count, Q
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.yields.models import YieldRecord
from apps.crops.models import ParcelCrop
from apps.parcels.models import Parcel
from apps.groups.models import MemberGroup, Group
from apps.weather.models import Alert as WeatherAlert

from ..models import IndicatorValue, Report


# ─── Résoudre l'organisation depuis l'utilisateur ────────────────────────────

def get_user_organisation(user):
    """
    Remonte la chaîne : user → MemberGroup (ACTIVE) → Group → Organisation.
    Priorité au rôle LEADER, sinon premier membership ACTIVE.
    Retourne None si aucune organisation trouvée.
    """
    # Priorité 1 : LEADER d'un groupe actif
    membership = (
        MemberGroup.objects
        .filter(user=user, status="ACTIVE", role__role_type="LEADER")
        .select_related("group__organisation")
        .first()
    )
    if membership:
        return membership.group.organisation

    # Priorité 2 : membre actif simple
    membership = (
        MemberGroup.objects
        .filter(user=user, status="ACTIVE")
        .select_related("group__organisation")
        .first()
    )
    if membership:
        return membership.group.organisation

    # Priorité 3 : créateur d'organisation
    return user.organisations_created.first()


def quarter_of(d):
    return f"T{(d.month - 1) // 3 + 1}-{d.year}"


# ─── Vue dashboard ────────────────────────────────────────────────────────────

class SEDashboardStatsView(APIView):
    """
    GET /api/suivi-evaluation/api/dashboard-stats/

    Toutes les stats S&E pour l'organisation de l'utilisateur connecté.
    Isolation totale : chaque organisation ne voit que ses propres données.
    """

    def get(self, request):
        today = timezone.now().date()
        current_quarter = quarter_of(today)

        # ── Résolution organisation ───────────────────────────────────────────
        organisation = get_user_organisation(request.user)

        if not organisation:
            return Response({
                "organisation":   None,
                "current_period": current_quarter,
                "kpis":           self._empty_kpis(),
                "chart":          {"unit": "kg/m²", "label": "Rendements", "data": []},
                "scorecard":      self._empty_scorecard(),
                "alerts":         [],
                "message":        "Aucune organisation rattachée à ce compte.",
            })

        # ── Parcelles de l'organisation ───────────────────────────────────────
        # Chemin : Parcel.owner → MemberGroup (ACTIVE) → Group → Organisation
        org_parcels = Parcel.objects.filter(
            owner__group_memberships__group__organisation=organisation,
            owner__group_memberships__status="ACTIVE",
        ).distinct()

        nb_parcelles = org_parcels.count()

        # ── Membres & groupes ─────────────────────────────────────────────────
        nb_membres_actifs = MemberGroup.objects.filter(
            group__organisation=organisation,
            status="ACTIVE",
        ).count()

        nb_groupes_actifs = Group.objects.filter(
            organisation=organisation,
            status="ACTIVE",
        ).count()

        # ── Cultures actives ──────────────────────────────────────────────────
        nb_cultures_actives = ParcelCrop.objects.filter(
            parcel__in=org_parcels,
        ).filter(
            Q(harvest_date__isnull=True) | Q(harvest_date__gte=today)
        ).count()

        # ── Rendements ────────────────────────────────────────────────────────
        org_yields = YieldRecord.objects.filter(parcelCrop__parcel__in=org_parcels)

        yield_stats = org_yields.aggregate(
            avg_yield=Avg("yield_amount"),
            total_yield=Sum("yield_amount"),
            total_area=Sum("area"),
            count=Count("id"),
        )
        avg_yield    = round(yield_stats["avg_yield"]   or 0, 2)
        total_yield  = round(yield_stats["total_yield"] or 0, 2)
        total_area   = yield_stats["total_area"] or 0
        nb_recoltes  = yield_stats["count"] or 0
        yield_per_m2 = round(total_yield / total_area, 4) if total_area > 0 else 0

        # ── Alertes météo ─────────────────────────────────────────────────────
        org_weather_alerts = WeatherAlert.objects.filter(
            parcel__in=org_parcels,
            is_read=False,
        )
        nb_alertes           = org_weather_alerts.count()
        nb_alertes_critiques = org_weather_alerts.filter(
            severity__in=["HIGH", "CRITICAL"]
        ).count()

        # ── Chart : évolution par trimestre ───────────────────────────────────
        yield_by_quarter: dict = {}
        for yr in org_yields.order_by("date"):
            q = quarter_of(yr.date)
            if q not in yield_by_quarter:
                yield_by_quarter[q] = {"sum": 0, "area": 0, "count": 0}
            yield_by_quarter[q]["sum"]   += yr.yield_amount
            yield_by_quarter[q]["area"]  += yr.area
            yield_by_quarter[q]["count"] += 1

        chart_data = []
        sorted_quarters = sorted(yield_by_quarter.keys())
        for i, q in enumerate(sorted_quarters):
            d   = yield_by_quarter[q]
            val = round(d["sum"] / d["area"], 4) if d["area"] > 0 else 0
            evolution = None
            if i > 0:
                prev_d   = yield_by_quarter[sorted_quarters[i - 1]]
                prev_val = round(prev_d["sum"] / prev_d["area"], 4) if prev_d["area"] > 0 else 0
                if prev_val > 0:
                    evolution = round(((val - prev_val) / prev_val) * 100, 2)
            chart_data.append({
                "period":        q,
                "value":         val,
                "total_kg":      round(d["sum"], 2),
                "count":         d["count"],
                "evolution_pct": evolution,
            })

        # ── Scorecard parcelles ───────────────────────────────────────────────
        parcel_evals = []
        for parcel in org_parcels[:50]:
            critical_w = WeatherAlert.objects.filter(
                parcel=parcel, severity__in=["HIGH", "CRITICAL"]
            ).count()
            total_w = WeatherAlert.objects.filter(parcel=parcel).count()

            compliance  = max(0.0, 100 - (critical_w * 25) - ((total_w - critical_w) * 10))
            parcel_avg  = YieldRecord.objects.filter(
                parcelCrop__parcel=parcel
            ).aggregate(avg=Avg("yield_amount"))["avg"] or 0
            yield_score = min((parcel_avg / avg_yield * 100), 100) if avg_yield > 0 else 0
            risk        = "HIGH" if critical_w >= 2 else (
                          "MEDIUM" if critical_w >= 1 or total_w >= 3 else "LOW")

            parcel_evals.append({
                "parcel_id":        str(parcel.uuid),
                "parcel_name":      parcel.parcel_name,
                "compliance_score": round(compliance, 1),
                "yield_score":      round(yield_score, 1),
                "risk_level":       risk,
            })

        if parcel_evals:
            avg_compliance  = sum(e["compliance_score"] for e in parcel_evals) / len(parcel_evals)
            avg_yield_score = sum(e["yield_score"]      for e in parcel_evals) / len(parcel_evals)
            risk_counts     = {"LOW": 0, "MEDIUM": 0, "HIGH": 0}
            for e in parcel_evals:
                risk_counts[e["risk_level"]] += 1
            low_pct = (risk_counts["LOW"] / len(parcel_evals)) * 100
        else:
            avg_compliance = avg_yield_score = low_pct = 0
            risk_counts    = {"LOW": 0, "MEDIUM": 0, "HIGH": 0}

        # ── Alertes S&E ───────────────────────────────────────────────────────
        se_alerts = []

        # Rapports DRAFT de l'organisation
        for r in Report.objects.filter(
            organisation_id=organisation.uuid,
            status=Report.ReportStatus.DRAFT,
        ).order_by("-created_at")[:10]:
            se_alerts.append({
                "id":          f"report-{r.uuid}",
                "title":       f'Rapport "{r.name}" non soumis',
                "description": f"Brouillon depuis le {r.created_at.strftime('%d/%m/%Y')}. À finaliser.",
                "type":        "warning",
                "icon":        "bx bx-edit",
                "date":        r.created_at.strftime("%d/%m/%Y"),
                "location":    None,
            })

        # Valeurs d'indicateurs rejetées
        for v in IndicatorValue.objects.filter(
            status="REJECTED"
        ).select_related("indicator").order_by("-created_at")[:10]:
            se_alerts.append({
                "id":          f"val-{v.uuid}",
                "title":       f"Valeur rejetée — {v.indicator.name}",
                "description": f"Valeur {v.value} ({v.period}) rejetée. Correction requise.",
                "type":        "critical",
                "icon":        "bx bx-x-circle",
                "date":        v.created_at.strftime("%d/%m/%Y"),
                "location":    None,
            })

        # Alertes météo critiques des parcelles de l'org
        for a in org_weather_alerts.filter(
            severity__in=["HIGH", "CRITICAL"]
        ).select_related("parcel")[:5]:
            se_alerts.append({
                "id":          f"weather-{a.id}",
                "title":       f"Alerte météo — {a.type}",
                "description": a.message,
                "type":        "critical",
                "icon":        "bx bx-cloud-lightning",
                "date":        a.created_at.strftime("%d/%m/%Y"),
                "location":    a.parcel.parcel_name if a.parcel_id else None,
            })

        order_map = {"critical": 0, "warning": 1, "info": 2}
        se_alerts.sort(key=lambda x: order_map.get(x["type"], 3))

        # ── Réponse ───────────────────────────────────────────────────────────
        return Response({
            "organisation": {
                "uuid":     str(organisation.uuid),
                "name":     organisation.name,
                "org_type": organisation.org_type,
            },
            "current_period": current_quarter,
            "kpis": {
                "nb_membres_actifs":    nb_membres_actifs,
                "nb_groupes_actifs":    nb_groupes_actifs,
                "nb_parcelles":         nb_parcelles,
                "nb_cultures_actives":  nb_cultures_actives,
                "nb_recoltes":          nb_recoltes,
                "avg_yield":            avg_yield,
                "total_yield_kg":       total_yield,
                "yield_per_m2":         yield_per_m2,
                "nb_alertes":           nb_alertes,
                "nb_alertes_critiques": nb_alertes_critiques,
            },
            "chart": {
                "unit":  "kg/m²",
                "label": "Rendement moyen par trimestre",
                "data":  chart_data,
            },
            "scorecard": {
                "total_parcelles":  len(parcel_evals),
                "avg_compliance":   round(avg_compliance, 1),
                "avg_yield_score":  round(avg_yield_score, 1),
                "low_risk_pct":     round(low_pct, 1),
                "risk_counts":      risk_counts,
                "parcelles":        parcel_evals,
            },
            "alerts": se_alerts,
        })

    def _empty_kpis(self):
        return {
            "nb_membres_actifs": 0, "nb_groupes_actifs": 0,
            "nb_parcelles": 0, "nb_cultures_actives": 0,
            "nb_recoltes": 0, "avg_yield": 0, "total_yield_kg": 0,
            "yield_per_m2": 0, "nb_alertes": 0, "nb_alertes_critiques": 0,
        }

    def _empty_scorecard(self):
        return {
            "total_parcelles": 0, "avg_compliance": 0, "avg_yield_score": 0,
            "low_risk_pct": 0, "risk_counts": {"LOW": 0, "MEDIUM": 0, "HIGH": 0},
            "parcelles": [],
        }