import csv
import json
import pathlib

import pytest
from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files import File
from django.urls import reverse
from environ import Env
from faker import Faker

BASE_DIR = pathlib.Path(__file__).parent.resolve()

fake = Faker()

environ = Env()
environ.read_env()

def pytest_configure(config):
    if not settings.configured:
        settings.configure(
            DEBUG=True,
            BASE_DIR=BASE_DIR,
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


@pytest.fixture(scope='session')
def authenticated_client():
    from rest_framework.test import APIClient

    user_model = get_user_model()
    user_model.objects.create_user(username='testuser', password='touparet')

    user = user_model.objects.first()
    if user is None:
        raise ValueError("User creation failed")
    
    if user is not None:
        user.set_password('touparet')
        user.save()

    client = APIClient()
    path = reverse('token_obtain_pair')
    response = client.post(
        path, {
            'username': user.username,
            'password': 'touparet'
        }
    )

    assert response.status_code == 200

    token = response.json()['access']
    client.headers = {'HTTP_AUTHORIZATION': f'Token {token}'}
    return client


@pytest.fixture
def json_data():
    return [
        {
            "name": "Alice", 
            "age": 30,
            "meta": '{"age": 30, "city": "New York"}'
        },
        {
            "name": "Bob", 
            "age": 25,
            "meta": '{"age": 30, "city": "New York"}'
        }
    ]


@pytest.fixture
def csv_file(tmp_path):
    filepath = tmp_path / 'test.csv'
    with filepath.open('w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['name', 'age'])
        writer.writerow(['Alice', 30])
        writer.writerow(['Bob', 25])
    return filepath


@pytest.fixture
def csv_django_file(csv_file):
    return File(open(csv_file, 'rb'))


@pytest.fixture
def json_file(tmp_path):
    filepath = tmp_path / 'test.json'
    with filepath.open('w', encoding='utf-8') as f:
        json.dump([{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}], f)
    return filepath

@pytest.fixture
def json_django_file(json_file):
    return File(open(json_file, 'rb'))
