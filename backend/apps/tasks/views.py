"""
apps/tasks/views.py
-------------------
ViewSets DRF + vue HTML template pour les tâches.
"""
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from django.db import models
from django.utils import timezone
from django.utils.decorators import method_decorator
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.core.mixins import CacheInvalidationMixin
from apps.crops.models import ParcelCrop
from apps.tasks.models import Task, TaskPriority, TaskStatus
from apps.groups.models import MemberGroup
from apps.tasks.serializers import TaskSerializer, TaskPrioritySerializer, TaskStatusSerializer


@method_decorator(name='list', decorator=swagger_auto_schema(tags=['Tâches & Travaux']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(tags=['Tâches & Travaux']))
@method_decorator(name='create', decorator=swagger_auto_schema(tags=['Tâches & Travaux']))
@method_decorator(name='update', decorator=swagger_auto_schema(tags=['Tâches & Travaux']))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(tags=['Tâches & Travaux']))
@method_decorator(name='destroy', decorator=swagger_auto_schema(tags=['Tâches & Travaux']))
class TaskStatusViewSet(CacheInvalidationMixin, viewsets.ModelViewSet):
    """Statuts de tâche — lecture publique."""
    queryset = TaskStatus.objects.all()
    serializer_class = TaskStatusSerializer
    permission_classes = [permissions.AllowAny]
    cache_prefix = 'task_status'


@method_decorator(name='list', decorator=swagger_auto_schema(tags=['Tâches & Travaux']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(tags=['Tâches & Travaux']))
@method_decorator(name='create', decorator=swagger_auto_schema(tags=['Tâches & Travaux']))
@method_decorator(name='update', decorator=swagger_auto_schema(tags=['Tâches & Travaux']))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(tags=['Tâches & Travaux']))
@method_decorator(name='destroy', decorator=swagger_auto_schema(tags=['Tâches & Travaux']))
class TaskPriorityViewSet(CacheInvalidationMixin, viewsets.ModelViewSet):
    """Priorités de tâche — lecture publique."""
    queryset = TaskPriority.objects.all()
    serializer_class = TaskPrioritySerializer
    permission_classes = [permissions.AllowAny]
    cache_prefix = 'task_priority'


@method_decorator(name='list', decorator=swagger_auto_schema(tags=['Tâches & Travaux']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(tags=['Tâches & Travaux']))
@method_decorator(name='create', decorator=swagger_auto_schema(tags=['Tâches & Travaux']))
@method_decorator(name='update', decorator=swagger_auto_schema(tags=['Tâches & Travaux']))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(tags=['Tâches & Travaux']))
@method_decorator(name='destroy', decorator=swagger_auto_schema(tags=['Tâches & Travaux']))
class TaskViewSet(CacheInvalidationMixin, viewsets.ModelViewSet):
    """Tâches — accès restreint au propriétaire de la parcelle."""
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['name', 'due_date', 'priority', 'status']
    cache_prefix = 'task'

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Task.objects.none()
        
        user = self.request.user
        # Tâches liées aux parcelles possédées en propre
        queryset = Task.objects.filter(parcelCrop__parcel__owner=user)
        
        # S'il est leader d'un groupe, il voit les tâches des membres
        led_groups = MemberGroup.objects.filter(
            user=user, 
            role__role_type='LEADER', 
            status='ACTIVE'
        ).values_list('group_id', flat=True)
        
        if led_groups.exists():
            member_ids = MemberGroup.objects.filter(
                group_id__in=led_groups, 
                status='ACTIVE'
            ).values_list('user_id', flat=True)
            
            queryset = Task.objects.filter(
                models.Q(parcelCrop__parcel__owner=user) | 
                models.Q(parcelCrop__parcel__owner_id__in=member_ids)
            ).distinct()

        return (
            queryset
            .select_related('parcelCrop', 'status', 'priority')
        )

    @swagger_auto_schema(
        operation_summary="Marquer comme terminé",
        tags=['Tâches & Travaux'],
        responses={200: openapi.Schema(type=openapi.TYPE_OBJECT, properties={
            'status': openapi.Schema(type=openapi.TYPE_STRING),
            'completed_at': openapi.Schema(type=openapi.FORMAT_DATETIME)
        })}
    )
    @action(detail=True, methods=['post'])
    def mark_done(self, request, pk=None):
        """Marque la tâche comme terminée via la méthode du proxy."""
        task = self.get_object()
        task.mark_as_done()
        return Response({
            'status': 'Task marked as done',
            'completed_at': task.completed_at,
        })

    @swagger_auto_schema(
        operation_summary="Tâches imminentes (24h)",
        operation_description="Retourne la liste des tâches à faire demain et envoie un email de rappel.",
        tags=['Tâches & Travaux'],
        responses={200: openapi.Schema(type=openapi.TYPE_OBJECT, properties={
            'notified_tasks': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING))
        })}
    )
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Notifie par email les tâches dues dans 24h."""
        tomorrow = timezone.now().date() + timedelta(days=1)
        tasks_due = Task.objects.filter(
            parcelCrop__parcel__owner=request.user,
            due_date=tomorrow,
        )
        for task in tasks_due:
            send_mail(
                subject=f"Tâche à faire demain : {task.name}",
                message=f"Votre tâche '{task.name}' est prévue pour le {task.due_date}.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[request.user.email],
            )
        return Response({'notified_tasks': [t.name for t in tasks_due]})

    @swagger_auto_schema(
        operation_summary="Statistiques tâches (Dashboard)",
        tags=['Tâches & Travaux'],
        responses={200: openapi.Schema(type=openapi.TYPE_OBJECT)}
    )
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """Résumé des tâches par statut et priorité pour le dashboard."""
        tasks = Task.objects.filter(parcelCrop__parcel__owner=request.user)
        return Response({
            'by_status': {
                s.name: tasks.filter(status=s).count()
                for s in TaskStatus.objects.all()
            },
            'by_priority': {
                p.name: tasks.filter(priority=p).count()
                for p in TaskPriority.objects.all()
            },
            
            'overdue_count': sum(1 for t in tasks if t.is_overdue()),  # ← NOUVEAU

        })


@login_required(login_url='login')
def tasks_view(request):
    """Vue HTML — page de suivi des tâches (conservée pour le template Django)."""
    parcel_crops = ParcelCrop.objects.filter(parcel__owner=request.user)
    tasks = (
        Task.objects
        .filter(parcelCrop__in=parcel_crops)
        .select_related('parcelCrop', 'status', 'priority')
    )
    return render(request, 'tasks.html', {'tasks': tasks or None})