from datetime import timedelta
from django.utils.timezone import now
from django.core.mail import send_mail
from events_project.celery import app
from events_app.models import Event
from django.contrib.auth import get_user_model

@app.task(name='api.send_email')
def send_email(to_email:str, subject:str, body:str):
    send_mail(
        subject,
        body,
        "noreply@example.com",
        [to_email],
        fail_silently=False,
    )

@app.task(name='api.check_events')
def check_events():
    """Напоминание за 24 часа и 6 часов"""
    events = Event.objects.all()
    now_time = now()

    for event in events:
        delta = event.meeting_time - now_time

        # за 24 часа
        if timedelta(hours=23, minutes=50) < delta < timedelta(hours=24, minutes=10):
            for user in event.users.all():
                send_email.delay(
                    user.email,
                    f"Напоминание: {event.name}",
                    f"Вы согласились посетить «{event.name}»!\n"
                    f"{event.description}\n"
                    f"Завтра в {event.meeting_time}, место: онлайн/офлайн",
                )
        # за 6 часов
        if timedelta(hours=5, minutes=50) < delta < timedelta(hours=5, minutes=10):
            for user in event.users.all():
                send_email.delay(
                    user.email,
                    f"Напоминание: {event.name}",
                    f"Вы идёте на «{event.name}»!\n"
                    f"{event.description}\n"
                    f"Сегодня в {event.meeting_time}, место: онлайн/офлайн",
                )

@app.task(name='api.send_new_event_notification')
def send_new_event_notification(event_id:int):
    """Уведомление о новом событии"""
    User = get_user_model()
    event = Event.objects.get(id=event_id)
    users = User.objects.filter(notify=True)

    for user in users:
        send_email.delay(
            user.email,
            f"Новое мероприятие: {event.name}!",
            f"{event.description}\n"
            f"Мероприятие завтра в {event.meeting_time}, место: онлайн/офлайн",
        )