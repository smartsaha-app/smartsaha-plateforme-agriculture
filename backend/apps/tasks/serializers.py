"""
apps/tasks/serializers.py
-------------------------
Serializers pour Task, TaskStatus, TaskPriority.
"""
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field, OpenApiTypes
from apps.tasks.models import Task, TaskPriority, TaskStatus


class TaskPrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskPriority
        fields = '__all__'


class TaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStatus
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    # Lecture imbriquée pour l'affichage
    priority_detail = TaskPrioritySerializer(source='priority', read_only=True)
    status_detail   = TaskStatusSerializer(source='status', read_only=True)

    # ✅ Champs calculés — méthodes maintenant définies sur le modèle
    is_done      = serializers.SerializerMethodField()
    is_overdue   = serializers.SerializerMethodField()
    days_overdue = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id', 'name', 'description', 'parcelCrop', 'due_date',
            'priority', 'priority_detail',
            'status', 'status_detail',
            'created_at', 'updated_at', 'completed_at',
            'is_done', 'is_overdue', 'days_overdue',
        ]
        read_only_fields = ['completed_at', 'history', 'created_at', 'updated_at']

    @extend_schema_field(OpenApiTypes.BOOL)
    def get_is_done(self, obj):
        return obj.is_done()

    @extend_schema_field(OpenApiTypes.BOOL)
    def get_is_overdue(self, obj):
        return obj.is_overdue()

    @extend_schema_field(OpenApiTypes.INT)
    def get_days_overdue(self, obj):
        return obj.days_overdue()

    def create(self, validated_data):
        task = Task.objects.create(**validated_data)
        task.add_history("Created")
        return task

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.add_history("Updated")
        instance.save()
        return instance
