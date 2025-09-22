from django.urls import path
from .views import UserRegisterView, UserListView, EventListView, EventSubscribeView, MyEventsView

urlpatterns = [
    # Пользователи
    path('users/register/', UserRegisterView.as_view(), name='user_register'),
    path('users/list/', UserListView.as_view(), name='user-list'),

    # События
    path('events/', EventListView.as_view(), name='event-list'),
    path('event/<int:pk>/subscribe/', EventSubscribeView.as_view(), name='event-subscribe'),
    path('events/my/', MyEventsView.as_view(), name='my-events'),
]