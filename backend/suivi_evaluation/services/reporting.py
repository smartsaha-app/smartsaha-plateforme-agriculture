"""
suivi_evaluation/services/reporting.py
--------------------------------------
Service de génération de rapports consolidés.
Agrège les données des différentes apps (parcels, crops, yields, tasks).
"""
from django.db.models import Sum, Count, Avg
from apps.parcels.models import Parcel
from apps.crops.models import ParcelCrop
from apps.tasks.models import Task
from apps.yields.models import YieldRecord
from ..models import Report, ReportData


class ReportGenerator:
    """
    Générateur de rapports pour une organisation sur une période donnée.
    """

    def __init__(self, report: Report):
        self.report = report
        self.org_id = report.organisation_id
        self.start = report.period_start
        self.end = report.period_end

    def generate(self):
        """
        Calcule les métriques et remplit ReportData.
        """
        # 1. Total Superficie (Ha) de l'organisation
        total_area = Parcel.objects.filter(
            owner__group_memberships__group__organisation_id=self.org_id
        ).distinct().aggregate(total=Sum('parcel_crops__area'))['total'] or 0.0
        self._add_data('TOTAL_HA', total_area)

        # 2. Nombre de producteurs actifs
        prod_count = Parcel.objects.filter(
            owner__group_memberships__group__organisation_id=self.org_id
        ).values('owner').distinct().count()
        self._add_data('PROD_COUNT', prod_count)

        # 3. Rendement Moyen (tonnes/ha) estimé
        yield_avg = YieldRecord.objects.filter(
            parcelCrop__parcel__owner__group_memberships__group__organisation_id=self.org_id,
            date__range=[self.start, self.end]
        ).aggregate(avg=Avg('yield_amount'))['avg'] or 0.0
        self._add_data('YIELD_AVG', yield_avg)

        # 4. Taux de complétion des tâches (%)
        tasks = Task.objects.filter(
            parcelCrop__parcel__owner__group_memberships__group__organisation_id=self.org_id,
            due_date__range=[self.start, self.end]
        )
        total_tasks = tasks.count()
        completed_tasks = tasks.filter(completed_at__isnull=False).count()
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        self._add_data('TASK_COMPLETION', completion_rate)

        # Mise à jour du statut du rapport
        self.report.status = Report.ReportStatus.APPROVED
        self.report.save()
        return self.report

    def _add_data(self, key, value):
        ReportData.objects.update_or_create(
            report=self.report,
            key=key,
            defaults={'value': value}
        )
