import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings.local')

app = Celery('setup')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'add-every-24-hours': {
        'task': 'apps.payment.tasks.check_payment_due_date',
        'schedule': crontab(minute=0, hour=0),
    },
}
