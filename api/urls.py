from django.urls import path
from .views import UserRegisterView, UserListView, EventListView, EventSubscribeView, MyEventsView

urlpatterns = [
    path('user/register/', UserRegisterView.as_view(), name='user_register'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('events/', EventListView.as_view(), name='event-list'),
    path('event/<int:pk>/', EventSubscribeView.as_view(), name='event-subscribe'),
    path('events/my/', MyEventsView.as_view(), name='my-events'),
]