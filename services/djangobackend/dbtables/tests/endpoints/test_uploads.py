import csv
import json

import pytest
from django.core.files import File
from django.urls import reverse
from rest_framework.test import APIClient

from dbtables.models import DatabaseTable
from dbtables.tests.constants import (
    JSONPLACEHOLDER_URL,
    OPENDATASOFT_COLUMN_TYPES,
    OPENDATASOFT_URL,
)
from dbtables.tests.utils import DatabaseTableFactory
from djangobackend.huey_app import huey_task

huey_task.immediate = True

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


@pytest.fixture
def table() -> DatabaseTable:
    return DatabaseTableFactory.create()


@pytest.fixture
def document_metadata():
    documents_metadata = [
        {
            'name': 'file_0',  # Matches the key in the root data dict
            'url': None,
            'source_type': 'file',
            'content_type': 'csv',
            'primary_key_field': False,
            'entry_key': None
        },
        {
            'name': 'file_1',  # Matches the key in the root data dict
            'url': None,
            'source_type': 'file',
            'content_type': 'csv',
            'primary_key_field': False,
            'entry_key': None
        }
    ]
    
    using_columns = [
        {
            'name': 'name',
            'newName': 'name',
            'unique': False,
            'visible': True,
            'nullable': True
        },
        {
            'name': 'age',
            'newName': 'age',
            'unique': False,
            'visible': True,
            'nullable': True
        }
    ]
    
    data = {
        'merge': 'False',
        'name': 'Test Table',
        'documents': json.dumps(documents_metadata),
        'column_options': json.dumps(using_columns),        
        'file_0': None,  
        'file_1': None,
    }
    return data


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
@pytest.mark.api
@UPLOAD_DATA
def test_upload_document_edge_cases(api_client: APIClient, table, upload_data):
    path = reverse('database_tables:upload_document', args=[table.pk])
    response = api_client.post(
        path,
        data=upload_data['data'],
        content_type='application/json'
    )
    assert response.status_code == upload_data['expected_status'], response.content


@pytest.mark.django_db
@pytest.mark.api
def test_upload_document_with_multiple_valid_csv_files(api_client: APIClient, document_metadata, table, csv_django_file):
    path = reverse('database_tables:upload_document', args=[table.pk])
    
    document_metadata['file_0'] = csv_django_file
    document_metadata['file_1'] = csv_django_file
    
    response = api_client.post(path, data=document_metadata)    
    assert response.status_code == 201, response.content
    assert 'documents' in response.json()


@pytest.mark.django_db
@pytest.mark.api
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
        },
        {
            'expected_status': 201,
            'description': 'Test content merging',
            'data': {
                'name': '',
                'using_columns': OPENDATASOFT_COLUMN_TYPES,
                'documents': [
                    {
                        'name': 'Json Data',
                        'url': JSONPLACEHOLDER_URL,
                        'file': None,
                        'entry_key': '',
                        'source_type': 'url',
                        'content_type': 'json',
                        # 'primary_document': True, # TODO: Add this field
                        'primary_key_field': False # TODO: Remove this field
                    },
                    {
                        'name': 'Json Data',
                        'url': JSONPLACEHOLDER_URL,
                        'file': None,
                        'entry_key': '',
                        'source_type': 'url',
                        'content_type': 'json',
                        # 'primary_document': True,
                        'primary_key_field': False
                    }
                ],
                'merge': True
            }
        }
    ]
)

@pytest.mark.django_db
@pytest.mark.api
@URL_DATA
def test_upload_via_url(api_client: APIClient, table, url_data):
    path = reverse('database_tables:upload_document', args=[table.pk])
    response = api_client.post(path, data=url_data['data'], content_type='application/json')
    assert response.status_code == url_data['expected_status'], response.content


@pytest.mark.django_db
@pytest.mark.api
def test_upload_file_via_google_sheet_id(api_client: APIClient, table):
    pass

