from rest_framework.routers import DefaultRouter

from .views import TaskViewSet, UserRegistrationViewSet

router = DefaultRouter()

router.register('auth/register', UserRegistrationViewSet, basename="registration")

router.register(r"api/v1/tasks", TaskViewSet, basename="tasks")
