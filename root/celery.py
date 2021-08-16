from __future__ import absolute_import, unicode_literals

from celery import Celery
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'root.settings')

app = Celery('root')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
