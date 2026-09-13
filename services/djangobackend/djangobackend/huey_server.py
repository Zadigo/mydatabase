import os
import pathlib

import django
from django.conf import settings
from django.utils.module_loading import autodiscover_modules

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangobackend.settings')

settings.configure(
    BASE_DIR=pathlib.Path(__file__).resolve().parent.parent,
    INSTALLED_APPS = [
        'daphne',

        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        'corsheaders',
        'django_celery_beat',
        'drf_spectacular',
        'import_export',
        'django_extensions',
        'graphene_django',
        'mcp_server',
        'oauth2_provider',
        'oauth_dcr',

        'rest_framework',
        'rest_framework.authtoken',

        'tabledocuments',
        'dbschemas',
        'dbtables',
        'endpoints'
    ]
)

if settings.configured:
    django.setup()

from djangobackend.huey_app import huey_task  # noqa

if __name__ == "__main__":
    autodiscover_modules("django_tasks")

