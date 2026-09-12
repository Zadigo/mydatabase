import pathlib

import pytest
from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator
from django.conf import settings
from faker import Faker

BASE_DIR = pathlib.Path(__file__).parent.resolve()

fake = Faker()

def pytest_configure(config):
    if not settings.configured:
        settings.configure(
            DEBUG=True,
            SECRET_KEY=fake.uuid4(),
            PY_UTILITIES_JWT_SECRET=fake.uuid4(),
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': ':memory:',
                }
            },
            INSTALLED_APPS=[
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
            ],
            AUTH_USER_MODEL='auth.User',
            ROOT_URLCONF='djangobackend.urls',
            DEFAULT_AUTO_FIELD='django.db.models.BigAutoField',
            REST_FRAMEWORK={
                'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
                'DEFAULT_AUTHENTICATION_CLASSES': [
                    'rest_framework_simplejwt.authentication.JWTAuthentication',
                    'rest_framework.authentication.TokenAuthentication',
                ]
            },
            SIMPLE_JWT={'AUTH_HEADER_TYPES': ['Token']},
            # IMAGEKIT_CACHEFILE_NAMER='imagekit.cachefiles.namers.hash',
            GRAPHENE={'SCHEMA': 'djangobackend.schema.schema'},
            STATIC_URL='/static/',
            MEDIA_ROOT=BASE_DIR / 'media',
        )


@pytest.fixture(scope='session')
def api_client():
    from rest_framework.test import APIClient
    client = APIClient()
    return client


@pytest.fixture(scope='session')
async def ws_router():
    from dbtables import routing as table_routing
    from tabledocuments import routing as document_routing
    router = URLRouter(document_routing.urlpatterns + table_routing.urlpatterns)
    return router


@pytest.fixture(scope='session')
async def ws_documents(ws_router):
    communicator = WebsocketCommunicator(ws_router, '/ws/databases/1/documents')
    state, _ = await communicator.connect()
    return communicator
