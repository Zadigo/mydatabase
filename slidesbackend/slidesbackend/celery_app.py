import os

from celery import Celery
from celery.schedules import crontab

# Windows: celery -A slidesbackend.celery_app worker -E --pool=solo
# Windows - Beat: celery -A slidesbackend.celery_app beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
# Windows - Flower: celery -A slidesbackend.celery_app flower

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'slidesbackend.settings')


def get_broker():
    from django.conf import settings
    return getattr(settings, 'CELERY_BROKER_URL')


def get_backend():
    from django.conf import settings
    return getattr(settings, 'CELERY_RESULT_BACKEND')


app = Celery(
    'slidesbackend',
    broker=get_broker(),
    backend=get_backend(),
    logger='celery_app.log'
)

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Europe/London',
    enable_utc=True
)

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {}
