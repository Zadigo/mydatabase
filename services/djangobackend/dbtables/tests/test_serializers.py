
from unittest.mock import patch

import pytest
from faker import Faker

from dbtables.api.serializers import UploadFileSerializer
from dbtables.tests.constants import UPLOAD_DOCUMENT_DATA

fake = Faker()

FAKE_DATA = {
    'name': fake.name(),
    'using_columns': [],
    'documents': [],
    'merge': False
}


@pytest.fixture
def base_data():
    return FAKE_DATA


@pytest.fixture
def data_with_columns():
    FAKE_DATA['using_columns'] = [
        {
            'name': 'firstname',
            'newName': 'firstname',
            'columnType': 'String',
            'unique': False,
            'visible': False,
            'nullable': False
        }
    ]

    FAKE_DATA['documents'] = [
        {
            'name': fake.name(),
            'url': '',
            'file': None,
            'entry_key': '',
            'source_type': 'url',
            'content_type': 'json',
            'primary_key_field': False
        }
    ]

    return FAKE_DATA


@pytest.fixture
def data_with_file():
    pass


def test_upload_serializer_base_data(base_data, data_with_columns):
    serializer = UploadFileSerializer(data=base_data)
    serializer.is_valid(raise_exception=False)

    assert serializer.errors == {}

    serializer = UploadFileSerializer(data=data_with_columns)
    serializer.is_valid(raise_exception=False)

    assert serializer.errors == {}



def test_upload_with_file(datafiles):
    print('datafiles', datafiles)



@pytest.fixture
def docs_to_merge():
    DOC1 = [
        {
            'id': 1,
            'name': fake.name()
        },
        {
            'id': 6,
            'name': fake.name()
        }
    ]

    DOC2 = [
        {
            'id': 6,
            'name': fake.name(),
            'age': fake.random_int(min=18, max=99),
        }
    ]

    return [DOC1, DOC2]


def test_upload_with_merge(docs_to_merge):
    with patch('tabledocuments.django_tasks.create_csv_file_from_data') as m:
        UPLOAD_DOCUMENT_DATA['merge'] = True
        UPLOAD_DOCUMENT_DATA['documents'] = [
            {
                'name': fake.name(),
                'url': '',
                'file': None,
                'entry_key': '',
                'source_type': 'url',
                'content_type': 'json',
                'primary_key_field': False
            }
        ]

        serializer = UploadFileSerializer(data=UPLOAD_DOCUMENT_DATA)
        serializer.is_valid(raise_exception=False)
        serializer._merge_documents(docs_to_merge)
