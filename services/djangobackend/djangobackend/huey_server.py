import os

import django
from django.utils.module_loading import autodiscover_modules

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangobackend.settings')

django.setup()

from djangobackend.huey_app import huey_task  # noqa

if __name__ == "__main__":
    autodiscover_modules("django_tasks")

