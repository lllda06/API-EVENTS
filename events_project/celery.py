import os
from celery import Celery


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", 'events_project.settings')

app = Celery('events_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.task_routes = {
    'api.tasks.send_email': {'queue': 'emails'},
    'api_tasks.send_new_event_notification': {'queue': 'emails'},
}


