"""
apps/users/urls.py
------------------
URLs de l'app users : CRUD profils + auth endpoints.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.users.views import (
    UserViewSet,
    SignupView,
    LoginView,
    LogoutView,
    GoogleLoginView,
    ForgotPasswordView,
    ResetPasswordView,
    ChangePasswordView,
    FarmerDirectoryViewSet,
    GenerateOTPView,
    VerifyOTPView,
    MobileSignupView,
    MobileVerifySignupView,
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'discovery-farmers', FarmerDirectoryViewSet, basename='discovery-farmers')

urlpatterns = [
    # CRUD profils
    path('', include(router.urls)),
    # Auth endpoints API
    path('signup/',                              SignupView.as_view(),        name='signup'),
    path('login/',                               LoginView.as_view(),         name='login'),
    path('logout/',                              LogoutView.as_view(),        name='logout'),
    path('google-login/',                        GoogleLoginView.as_view(),   name='google-login'),
    path('forgot-password/',                     ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/',                      ResetPasswordView.as_view(), name='reset-password'),
    path('change-password/',                     ChangePasswordView.as_view(), name='change-password'),
    # Auth Mobile OTP Endpoints
    path('auth_mobile/',                         GenerateOTPView.as_view(),        name='generate-otp'),
    path('verify_otp/',                          VerifyOTPView.as_view(),          name='verify-otp'),
    # Inscription Mobile (OTP à l'inscription uniquement)
    path('mobile/signup/',                       MobileSignupView.as_view(),       name='mobile-signup'),
    path('mobile/verify-signup/',                MobileVerifySignupView.as_view(), name='mobile-verify-signup'),
]