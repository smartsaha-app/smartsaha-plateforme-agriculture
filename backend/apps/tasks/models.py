"""
apps/tasks/models.py
--------------------
Modèles pour les tâches, priorités et statuts.
"""
from django.db import models
from django.utils import timezone


class TaskPriority(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        verbose_name = 'Priorité'
        verbose_name_plural = 'Priorités'
        ordering = ['id']

    def __str__(self):
        return self.name


class TaskStatus(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        verbose_name = 'Statut de tâche'
        verbose_name_plural = 'Statuts de tâche'
        ordering = ['id']

    def __str__(self):
        return self.name


class Task(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    parcelCrop = models.ForeignKey(
        'crops.ParcelCrop',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='tasks'
    )
    due_date = models.DateField()
    priority = models.ForeignKey(
        'TaskPriority',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='tasks'
    )
    status = models.ForeignKey(
        'TaskStatus',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='tasks'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    history = models.JSONField(default=list, blank=True)

    class Meta:
        verbose_name = 'Tâche'
        verbose_name_plural = 'Tâches'
        ordering = ['-created_at']

    def __str__(self):
        priority_name = self.priority.name if self.priority else 'Aucune priorité'
        status_name = self.status.name if self.status else 'Aucun statut'
        return f"{self.name} - {self.due_date} - {priority_name} - {status_name}"

    # ✅ CORRIGÉ : méthodes restaurées depuis le code commenté
    def is_done(self) -> bool:
        """Retourne True si la tâche a été complétée."""
        return self.completed_at is not None

    def is_overdue(self) -> bool:
        """Retourne True si la date d'échéance est dépassée et non terminée."""
        if self.is_done():
            return False
        return self.due_date < timezone.now().date()

    def days_overdue(self) -> int | None:
        """Retourne le nombre de jours de retard, ou None si à jour."""
        if not self.is_overdue():
            return None
        return (timezone.now().date() - self.due_date).days

    def mark_as_done(self):
        """Marquer la tâche comme terminée."""
        done_status = TaskStatus.objects.filter(name__iexact="Done").first()
        if done_status:
            self.status = done_status
            self.completed_at = timezone.now()
            self.add_history("Marked as Done")
            self.save()

    def add_history(self, action: str):
        """Ajouter une entrée à l'historique de la tâche."""
        self.history.append({
            "action": action,
            "timestamp": timezone.now().isoformat()
        })
        self.save()
