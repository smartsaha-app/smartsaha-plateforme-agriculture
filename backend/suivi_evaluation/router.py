# suivi_evaluation/router.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import reporting, evaluation, datalog, indicators
from .views.dashboard import SEDashboardStatsView

router = DefaultRouter()

# Indicators
router.register(r'indicator-categories', indicators.IndicatorCategoryViewSet)
router.register(r'indicators', indicators.IndicatorViewSet)
router.register(r'indicator-values', indicators.IndicatorValueViewSet)

# Reporting
router.register(r'reporting', reporting.ReportViewSet)
router.register(r'report-data', reporting.ReportDataViewSet)
router.register(r'report-attachments', reporting.ReportAttachmentViewSet)

# Certifications
router.register(r'certification-types', evaluation.CertificationTypeViewSet)
router.register(r'certification-audits', evaluation.CertificationAuditViewSet)
router.register(r'certifications', evaluation.CertificationViewSet)

# Data management
router.register(r'datalogs', datalog.DataLogViewSet)
router.register(r'custom-fields', datalog.CustomFieldViewSet)
router.register(r'custom-field-values', datalog.CustomFieldValueViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    # Dashboard stats — lit directement yields, parcels, groups, weather
    path('api/dashboard-stats/', SEDashboardStatsView.as_view(), name='se-dashboard-stats'),
]