from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=300, null=True, blank=True)
    completed = models.BooleanField(default=False)


# class TechParkParticipants(Model):
#     pass
