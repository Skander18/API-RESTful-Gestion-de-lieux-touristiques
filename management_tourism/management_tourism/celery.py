import os
from celery import Celery
from celery.schedules import crontab
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'management_tourism.settings')
django.setup()

app = Celery('management_tourism')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Planifier la tâche pour s'exécuter toutes les heures
app.conf.beat_schedule = {
    'send_report_every_hour': {
        'task': 'locations.tasks.send_hourly_report',
        'schedule': crontab(minute=0, hour='*'),  # Chaque heure
    },
}
