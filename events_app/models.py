from django.db import models

from django.db import models
from django.conf import settings

class Event(models.Model):
    name = models.CharField(max_length=255)
    meeting_time = models.DateTimeField()
    description = models.TextField(blank=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="events", blank=True)

    def __str__(self):
        return f"{self.name} @ {self.meeting_time}"