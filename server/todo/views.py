from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import CreateModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from typing import Any

from .filters import TaskFilter
from .models import Task, User
from .serializers import (
    TaskSerializer,
    UserRegistrationSerializer,
    RepresentationSerializer,
)
from .services import TechParkParticipantsService, TechParkParticipantsServiceException


class UserRegistrationViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = UserRegistrationSerializer
    permission_classes = ()
    queryset = User.objects.order_by("id")


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter

    def get_queryset(self) -> QuerySet:
        return Task.objects.order_by("id")

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter("completed", openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN),
            openapi.Parameter("title", openapi.IN_QUERY, type=openapi.TYPE_STRING),
        ]
    )
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().list(request, *args, **kwargs)


class TechParkParticipantsViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = RepresentationSerializer

    def perform_create(self, serializer: BaseSerializer) -> None:
        try:
            TechParkParticipantsService.create_participants()
        except TechParkParticipantsServiceException as exc:
            raise ValidationError(str(exc)) from exc
