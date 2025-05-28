import os

from celery import Celery


# set the default Django settings module for the 'celery' app.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prowlscan.settings')

app = Celery('prowlscan')

# Using a string here means the worker doesn't have to serialize the configuration object to child processes.
# read config from Django settings, the CELERY namespace would make celery config keys have `CELERY` prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# discover and load tasks.py from from all registered Django apps
app.autodiscover_tasks()
