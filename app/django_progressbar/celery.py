import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_progressbar.settings")

# Celery app作成
# project名, brokerのホストを指定
app = Celery("django_progressbar", broker="redis://redis:6379/0")
app.conf.result_backend = "redis://redis:6379/0"

# app = Celery("django_progressbar", broker="redis://localhost:6379/0") # for localhost
# app.conf.result_backend = "redis://localhost:6379/0"


# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
