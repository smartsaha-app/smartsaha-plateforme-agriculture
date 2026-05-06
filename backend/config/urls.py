"""
config/urls.py
--------------
État : Phase 2 du démantèlement terminée.
- SmartSaha/views/ vidé → toutes les routes passent par /api/v2/
- apps/chatbot/ et apps/dashboard/ créés et branchés
- Les routes legacy HTML sont conservées (dashboard/, assistant-agronome/)
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework import permissions

# ── Apps v2 ──────────────────────────────────────────────────────────────────
from apps.users.views import (
    SignupView,
    LoginView,
    GoogleLoginView,
    ForgotPasswordView,
    ResetPasswordView,
)
from apps.dashboard.views import dashboard
from apps.chatbot.views import assistant_agronome_page, assistant_agronome_api


def redirect_to_swagger(request):
    return redirect('swagger-ui')



urlpatterns = [
    # ── Racine & Swagger ─────────────────────────────────────────────────────
    path('', redirect_to_swagger, name='home'),
    
    # Swagger UI (drf-spectacular)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # Redirection de l'ancienne URL
    path('swagger/', lambda request: redirect('swagger-ui'), name='old-swagger'),

    # ── Admin ────────────────────────────────────────────────────────────────
    path('admin/', admin.site.urls),

    # ── Auth (Pages HTML) ────────────────────────────────────────────────────
    path('login/',  auth_views.LoginView.as_view(template_name='login.html'), name='login-html'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login-html'),    name='logout'),

    # ── API v2 — Toutes les ressources ───────────────────────────────────────
    path('api/', include('apps.users.urls')),
    path('api/', include('apps.parcels.urls')),
    path('api/', include('apps.crops.urls')),
    path('api/', include('apps.tasks.urls')),
    path('api/', include('apps.yields.urls')),
    path('api/', include('apps.groups.urls')),
    path('api/', include('apps.weather.urls')),
    path('api/', include('apps.dashboard.urls')),
    path('api/', include('apps.chatbot.urls')),
    path('api/', include('apps.fire.urls')),
    path('api/marketplace/', include('apps.marketplace.urls')),
    path('api/kyc/',         include('apps.kyc.urls')),
    path('api/messaging/',   include('apps.messaging.urls')),
    path('api/mobile/payments/', include('apps.payments.urls')),

    # ── Suivi-évaluation (App indépendante) ──────────────────────────────────
    path('api/suivi-evaluation/', include('suivi_evaluation.router')),

    # ── Pages HTML Legacy (Conservées pour le moment) ────────────────────────
    path('dashboard/',          dashboard,               name='dashboard'),
    path('assistant-agronome/', assistant_agronome_page, name='assistant_agronome_page'),

    # ── Endpoint legacy chatbot
    path('api/assistant-agronome/', assistant_agronome_api, name='assistant_agronome_api'),
]

from django.urls import re_path
from django.views.static import serve

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]