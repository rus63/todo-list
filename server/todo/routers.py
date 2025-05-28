from rest_framework.routers import DefaultRouter

from .views import TaskViewSet, UserRegistrationViewSet, TechParkParticipantsViewSet

router = DefaultRouter()

router.register("auth/register", UserRegistrationViewSet, basename="registration")

router.register(r"api/v1/tasks", TaskViewSet, basename="tasks")
router.register(
    r"api/v1/tech-park/participants",
    TechParkParticipantsViewSet,
    basename="tech_park_participants",
)
