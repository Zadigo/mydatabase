from django.test import TestCase
from django.test import override_settings
from dbtables.api import serializers
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import Mock, patch

from dbtables.tests.utils import DatabaseTableFactory

@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class TestUploadFileSerializer(TestCase):
    def setUp(self):
        table = DatabaseTableFactory.create()

        request = Mock()
        request.parser_context = {'kwargs': {'pk': table.pk}}
        self._context = {'request': request}
        self.request = request

        self.data = {
            'name': None,
            'file': None,
            'url': '',
            'google_sheet_id': '',
            'using_columns': [
                {
                    'name': 'col1',
                    'newName': 'col1',
                    'columnType': 'String',
                    'unique:': True,
                    'visible': True,
                    'nullable': False
                },
                {
                    'name': 'col2',
                    'newName': 'col2',
                    'columnType': 'String',
                    'unique:': True,
                    'visible': True,
                    'nullable': False
                }
            ]
        }

    def test_validate_file_size(self):
        pass

    def test_serializer_save_with_json(self):
        data = '{"col1": ["val1"], "col2": ["val2"]}'
        content_file = SimpleUploadedFile("test.json", data.encode('utf-8'))
        self.request.FILES = {'file': content_file}
        
        self.data['name'] = 'test.json'
        self.data['file'] = content_file

        serializer = serializers.UploadFileSerializer(data=self.data)
        serializer._context = self._context
        serializer.is_valid(raise_exception=True)

        with patch('dbtables.api.serializers.tasks.create_json_file_from_data') as mcreate_json:
            document = serializer.save()
            self.assertIsNotNone(document)

    def test_serializer_save_with_csv(self):
        data = b'col1,col2\nval1,val2'
        content_file = SimpleUploadedFile("test.csv", data)
        self.request.FILES = {'file': content_file}

        self.data['name'] = 'test.csv'
        self.data['file'] = content_file

        serializer = serializers.UploadFileSerializer(data=self.data)
        serializer._context = self._context
        serializer.is_valid(raise_exception=True)

        with patch('dbtables.api.serializers.tasks.create_csv_file_from_data') as mcreate_csv:
            document = serializer.save()
            self.assertIsNotNone(document)
