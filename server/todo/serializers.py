from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

from .models import Task, User


class TaskSerializer(ModelSerializer):
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)

    class Meta:
        model = Task
        fields = ("id", "title", "description", "completed", "updated_at")


class UserRegistrationSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    @transaction.atomic
    def create(self, validated_data) -> User:
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)
        return user

    def validate(self, attrs: dict) -> dict:
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Passwords don't match."})
        validate_password(attrs["password"])
        return attrs

    class Meta:
        model = User
        fields = ("id", "email", "password", "password2", "first_name", "last_name")


class RepresentationSerializer(Serializer):
    pass
