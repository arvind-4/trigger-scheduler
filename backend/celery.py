import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'check-scheduled-triggers': {
        'task': 'triggers.tasks.run_scheduled_triggers',
        'schedule': crontab(minute='*'),
    },
    'manage-event-logs': {
        'task': 'triggers.tasks.manage_event_logs',
        'schedule': crontab(minute='0', hour='*'),
    },
}