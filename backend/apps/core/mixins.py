"""
apps/core/mixins.py
-------------------
Mixins réutilisables pour les ViewSets DRF.
"""
from django.core.cache import cache
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend


class CacheInvalidationMixin:
    """
    Gère le cache automatique des ViewSets DRF.
    - Cache les endpoints list et retrieve.
    - Invalide le cache sur create/update/destroy.

    Usage :
        class ParcelViewSet(CacheInvalidationMixin, BaseModelViewSet):
            cache_prefix = "parcel"
            cache_timeout = 60 * 15  # 15 minutes
    """
    cache_timeout = 60 * 10   # 10 minutes par défaut
    cache_prefix = None        # À définir dans chaque ViewSet
    use_object_cache = False   # True = cache par pk pour retrieve

    def get_cache_key(self, suffix):
        return f"{self.cache_prefix}:{suffix}"

    def list(self, request, *args, **kwargs):
        # On inclut les query params pour éviter de servir la page 1 pour la page 2, etc.
        query_params = request.query_params.urlencode()
        key = self.get_cache_key(f"list:{query_params}")
        data = cache.get(key)
        if data:
            return Response(data)
        response = super().list(request, *args, **kwargs)
        cache.set(key, response.data, self.cache_timeout)
        return response

    def retrieve(self, request, *args, **kwargs):
        if self.use_object_cache:
            key = self.get_cache_key(f"detail:{kwargs.get('pk')}")
            data = cache.get(key)
            if data:
                return Response(data)
            response = super().retrieve(request, *args, **kwargs)
            cache.set(key, response.data, self.cache_timeout)
            return response
        return super().retrieve(request, *args, **kwargs)

    def invalidate_cache(self, obj=None):
        keys = cache.keys(f"{self.cache_prefix}:*") or []
        for k in keys:
            cache.delete(k)
        if obj:
            if hasattr(obj, "uuid"):
                cache.delete(self.get_cache_key(f"detail:{obj.uuid}"))
            if hasattr(obj, "parcel") and obj.parcel and hasattr(obj.parcel, "uuid"):
                cache.delete(f"parcel_full_data_{obj.parcel.uuid}")

    def perform_create(self, serializer):
        serializer.save()
        self.invalidate_cache(serializer.instance)

    def perform_update(self, serializer):
        serializer.save()
        self.invalidate_cache(serializer.instance)

    def perform_destroy(self, instance):
        self.invalidate_cache(instance)
        instance.delete()


class BaseModelViewSet(viewsets.ModelViewSet):
    """
    ViewSet de base commun à toutes les apps.
    Fournit : permissions, filtres, recherche, ordering, auto-fill created_by.

    Usage :
        class ParcelViewSet(CacheInvalidationMixin, BaseModelViewSet):
            queryset = Parcel.objects.all()
            serializer_class = ParcelSerializer
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ["created_at", "updated_at"]
    search_fields = ["name"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
