from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webscrape_the_one.settings')

app = Celery('webscrape_the_one')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# app.conf.beat_schedule = {
#     'scrape-every-minute': {
#         'task': 'the_one.tasks.scrape_periodically',
#         'schedule': crontab(),
#     }
# }
