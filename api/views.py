from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import get_object_or_404


from .serializers import RegisterSerializer, UserSerializer, EventSerializer, MyEventSerializer
from events_app.models import Event
from django.contrib.auth import get_user_model

User = get_user_model()

#Регистрация пользователя
class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

#Список всех пользователей (только админам)
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)

#Список будущих событий
class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        now = timezone.now()
        return Event.objects.filter(meeting_time__gte=now).order_by('meeting_time')

#Подписаться / отписаться от события (APIView с POST и DELETE)
class EventSubscribeView(generics.ListAPIView):
    queryset = Event.objects.all()
    permission_classes = (IsAuthenticated,)

    #POST — подписка
    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        now = timezone.now()
        if event.meeting_time <= now:
            return Response({'detail': 'Нельзя подписаться на прошедшее событие.'},
                            status=status.HTTP_400_BAD_REQUEST)
        if request.user in event.users.all():
            return Response({'detail': 'Вы уже подписаны.'}, status=status.HTTP_200_OK)
        event.users.add(request.user)
        return Response(EventSerializer(event).data, status=status.HTTP_200_OK)

    #DELETE — отписка
    def delete(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        if request.user not in event.users.all():
            return Response({'detail': 'Вы не подписаны на это событие!'}, status.HTTP_400_BAD_REQUEST)
        event.users.remove(request.user)
        return Response({'detail':'Вы успешно отписались от события.'}, status=status.HTTP_200_OK)

#Мои события - подписки пользователя
class MyEventsView(generics.ListAPIView):
    serializer_class = MyEventSerializer
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        now = timezone.now()
        return self.request.user.events.filter(meeting_time__gt=now).order_by('meeting_time')
