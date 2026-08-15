# from unittest.mock import Mock, patch

# from django.core.files.uploadedfile import SimpleUploadedFile
# from django.test import TestCase, override_settings

# from dbtables.api import serializers
# from dbtables.tests.utils import DatabaseTableFactory
import pathlib

import pytest
from django.conf import settings
from faker import Faker

from dbtables.api.serializers import UploadFileSerializer

fake = Faker()

FAKE_DATA = {
    'name': fake.name(),
    'using_columns': [],
    'documents': [],
    'merge': False
}

DATA_FILES = pytest.mark.datafiles(
    pathlib.Path(settings.MEDIA_ROOT).joinpath('testfile.json')
)


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



@DATA_FILES
def test_upload_with_file(datafiles):
    print('datafiles', datafiles)

# @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
# class TestUploadFileSerializer(TestCase):
#     def setUp(self):
#         table = DatabaseTableFactory.create()

#         request = Mock()
#         request.parser_context = {'kwargs': {'pk': table.pk}}
#         self._context = {'request': request}
#         self.request = request

#         self.data = {
#             'name': None,
#             'file': None,
#             'url': '',
#             'google_sheet_id': '',
#             'using_columns': [
#                 {
#                     'name': 'col1',
#                     'newName': 'col1',
#                     'columnType': 'String',
#                     'unique:': True,
#                     'visible': True,
#                     'nullable': False
#                 },
#                 {
#                     'name': 'col2',
#                     'newName': 'col2',
#                     'columnType': 'String',
#                     'unique:': True,
#                     'visible': True,
#                     'nullable': False
#                 }
#             ]
#         }

#     def test_validate_file_size(self):
#         pass

#     def test_serializer_save_with_json(self):
#         data = '{"col1": ["val1"], "col2": ["val2"]}'
#         content_file = SimpleUploadedFile("test.json", data.encode('utf-8'))
#         self.request.FILES = {'file': content_file}
        
#         self.data['name'] = 'test.json'
#         self.data['file'] = content_file

#         serializer = serializers.UploadFileSerializer(data=self.data)
#         serializer._context = self._context
#         serializer.is_valid(raise_exception=True)

#         with patch('dbtables.api.serializers.tasks.create_json_file_from_data') as mcreate_json:
#             document = serializer.save()
#             self.assertIsNotNone(document)

#     def test_serializer_save_with_csv(self):
#         data = b'col1,col2\nval1,val2'
#         content_file = SimpleUploadedFile("test.csv", data)
#         self.request.FILES = {'file': content_file}

#         self.data['name'] = 'test.csv'
#         self.data['file'] = content_file

#         serializer = serializers.UploadFileSerializer(data=self.data)
#         serializer._context = self._context
#         serializer.is_valid(raise_exception=True)

#         with patch('dbtables.api.serializers.tasks.create_csv_file_from_data') as mcreate_csv:
#             document = serializer.save()
#             self.assertIsNotNone(document)
