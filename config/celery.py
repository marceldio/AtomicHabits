from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

# Указываем настройки Django для Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")

# Используем настройки Django в Celery
app.config_from_object("django.conf:settings", namespace="CELERY")

# Автоматически обнаруживаем задачи в приложениях
app.autodiscover_tasks()
