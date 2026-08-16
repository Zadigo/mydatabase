import csv
import pathlib

import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework.test import APIClient

from dbtables.models import DatabaseTable
from dbtables.tests.constants import OPENDATASOFT_COLUMN_TYPES, OPENDATASOFT_URL
from dbtables.tests.utils import DatabaseTableFactory
from djangobackend.huey_app import huey_task

huey_task.immediate = True

@pytest.fixture
def csv_file():
    filename = 'test.csv'
    filepath = pathlib.Path(settings.MEDIA_ROOT) / filename
    with open(filepath, mode='w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['name', 'age'])
        writer.writerow(['Alice', 30])
        writer.writerow(['Bob', 25])
    return filepath


@pytest.fixture
def table() -> DatabaseTable:
    return DatabaseTableFactory.create()


UPDATE_DATA = pytest.mark.parametrize(
    "update_data",
    [
        {
            'expected_status': 200,
            'description': 'Update table name successfully',
            'data': {
                'name': 'Updated Table Name'
            }
        },
        # {
        #     'description': 'No database table with this id exists',
        #     'data': {
        #         'name': 'Updated Table Name'
        #     }
        # }
    ]
)

@pytest.mark.django_db
@UPDATE_DATA
def test_udpate_table(api_client: APIClient, table, update_data):
    path = reverse('database_tables:update_table', args=[table.pk])
    response = api_client.patch(path, data=update_data['data'], format='json')
    assert response.status_code == update_data['expected_status'], f"Response: {response.json()}"

    data = response.json()
    assert 'name' in data
    assert 'documents' in data
    assert data['name'] == update_data['data']['name']


UPLOAD_DATA = pytest.mark.parametrize(
    "upload_data",
    [
        {
            'expected_status': 400,
            'description': 'Both file and url cannot be None',
            'data': {
                'file': None,
                'url': None
            }
        }
    ]
)


@pytest.mark.django_db
@UPLOAD_DATA
def test_upload_document(api_client: APIClient, table, upload_data):
    path = reverse('database_tables:upload_document', args=[table.pk])
    response = api_client.post(
        path,
        data=upload_data['data'],
        content_type='application/json'
    )
    assert response.status_code == upload_data['expected_status'], response.content


@pytest.mark.django_db
def test_upload_file_via_csv(api_client: APIClient, table, csv_file):
    path = reverse('database_tables:upload_document', args=[table.pk])
    with csv_file.open('rb') as f:
        response = api_client.post(path, data={'file': f}, format='multipart')
    assert response.status_code == 400, response.content


URL_DATA = pytest.mark.parametrize(
    "url_data",
    [
        {
            'expected_status': 201,
            'description': 'No documents provided',
            'data': {
                'name': '',
                'using_columns': [],
                'documents': [],
                'merge': False
            }
        },
        {
            'expected_status': 201,
            'description': 'One document points to a valid JSON file',
            'data': {
                'name': '',
                'using_columns': OPENDATASOFT_COLUMN_TYPES,
                'documents': [
                    {
                        'name': 'Open Data',
                        'url': OPENDATASOFT_URL,
                        'file': None,
                        'entry_key': 'results',
                        'source_type': 'url',
                        'content_type': 'json',
                        'primary_key_field': False
                    }
                ],
                'merge': False
            }
        }
    ]
)

@pytest.mark.django_db
@URL_DATA
def test_upload_via_url(api_client: APIClient, table, url_data):
    path = reverse('database_tables:upload_document', args=[table.pk])
    response = api_client.post(path, data=url_data['data'], content_type='application/json')
    assert response.status_code == url_data['expected_status'], response.content


@pytest.mark.django_db
def test_upload_file_via_google_sheet_id(api_client: APIClient, table):
    pass



# class TestCheckoutDocument(TransactionTestCase):
#     # fixtures = ['fixtures/databases']
    
#     def setUp(self):
#         self.table: DatabaseTable = DatabaseTableFactory.create()

#         file_content = b'name,age\nAlice,30\nBob,25'
#         self.content_file = ContentFile(file_content, name='test.csv')

#     def test_checkout_file(self):
#         path = reverse('database_tables:checkout_document', args=[self.table.pk])
#         response = self.client.post(path, data={'file': self.content_file})
#         self.assertEqual(response.status_code, 200, response.content)
#         self.assertIn('sample', response.json())
#         self.assertIn('columns', response.json())
