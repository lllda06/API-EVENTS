from rest_framework import serializers
from events_app.models import User
from events_app.models import Event


# сериализатор для отображения пользователей

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# сериализатор для регистрации новых пользователей

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )

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