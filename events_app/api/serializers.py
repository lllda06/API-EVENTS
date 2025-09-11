from rest_framework import serializers
from django.contrib.auth.models import User
from events_app.models import Event


# сериализатор для отображения пользователей

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# сериализатор для регистрации новых пользователей

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data, ):
        # Создание пользователя через встроенный метод,
        # чтобы пароль хранился в зашифрованном виде (хэш)
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user

# сериализатор для событий без списка пользователей, которые подписались

class EventSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Event
        fields = ['id', 'name', 'meeting_time', 'description', 'users']

#сериализатор для просмотра событий, на которые я подписана со списком пользователей, которые подписались
class MyEventSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'name', 'meeting_time', 'description', 'users']