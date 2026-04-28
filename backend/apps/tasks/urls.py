from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.tasks.views import (
    TaskViewSet, TaskStatusViewSet, TaskPriorityViewSet, tasks_view
)

router = DefaultRouter()
router.register(r'tasks',          TaskViewSet,         basename='task')
router.register(r'task-status',    TaskStatusViewSet,   basename='task-status')
router.register(r'task-priority',  TaskPriorityViewSet, basename='task-priority')

urlpatterns = [
    path('', include(router.urls)),
    # Vue HTML template — accessible sur /tasks/
    path('tasks/', tasks_view, name='tasks'),
]