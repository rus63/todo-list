from typing import Any

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUserManager(BaseUserManager):
    def _create_user(self, email: str, password: str, **extra_fields: Any) -> "User":
        if not email:
            raise ValueError("The given email must be set.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self, email: str, password: str = None, **extra_fields: Any
    ) -> "User":
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(
        self, email: str, password: str = None, **extra_fields: Any
    ) -> "User":
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()


class Task(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=300, null=True, blank=True)
    completed = models.BooleanField(default=False)
    updated_at = models.DateTimeField(null=True, auto_now=True)

    def __str__(self) -> str:
        return f"{self.id} - {self.title}"


class TechParkParticipants(models.Model):
    serial_number = models.IntegerField(unique=True, null=False, blank=False)
    join_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    bin = models.BigIntegerField(null=False, blank=False)
    status = models.BooleanField(default=True, null=False, blank=False)
    company_name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self) -> str:
        return str(self.serial_number)
