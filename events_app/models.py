from django.db import models
from rest_framework import serializers

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class Event(models.Model):
    name = models.CharField(max_length=255)
    meeting_time = models.DateTimeField()
    description = models.TextField(blank=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="events", blank=True)

    def __str__(self):
        return f"{self.name} @ {self.meeting_time}"

class User(AbstractUser):
    notify = models.BooleanField(default=True)

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']  # убрали все связи, чтобы DRF не падал

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user
