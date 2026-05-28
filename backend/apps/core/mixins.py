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

    Fonctionne avec tous les backends Django (DatabaseCache, Redis, Memcached…).
    L'invalidation repose sur un compteur de version plutôt que sur cache.keys()
    (méthode Redis-only absente de DatabaseCache).

    Usage :
        class ParcelViewSet(CacheInvalidationMixin, BaseModelViewSet):
            cache_prefix = "parcel"
            cache_timeout = 60 * 15  # 15 minutes
    """
    cache_timeout = 60 * 10   # 10 minutes par défaut
    cache_prefix = None        # À définir dans chaque ViewSet
    use_object_cache = False   # True = cache par pk pour retrieve

    # ── Version ────────────────────────────────────────────────────────────
    def _version_key(self):
        return f"{self.cache_prefix}:_v"

    def _current_version(self):
        return cache.get(self._version_key(), 0)

    def _bump_version(self):
        """Incrémente la version → toutes les clés précédentes deviennent invalides."""
        v = self._current_version() + 1
        # Durée de vie longue : la version doit survivre aux données cachées
        cache.set(self._version_key(), v, self.cache_timeout * 4)
        return v

    # ── Clé versionnée ──────────────────────────────────────────────────────
    def get_cache_key(self, suffix):
        v = self._current_version()
        return f"{self.cache_prefix}:v{v}:{suffix}"

    # ── Endpoints cachés ────────────────────────────────────────────────────
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

    # ── Invalidation ────────────────────────────────────────────────────────
    def invalidate_cache(self, obj=None):
        # Incrémenter la version suffit : toutes les clés de l'ancienne version
        # deviennent inaccessibles sans avoir à les lister (pas besoin de cache.keys()).
        self._bump_version()
        if obj:
            # Suppression ciblée des éventuels caches de parcelle parente
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
