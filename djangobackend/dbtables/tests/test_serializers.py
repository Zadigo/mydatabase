from django.test import TestCase
from django.test import override_settings
from dbtables.api import serializers
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import Mock, patch

from dbtables.tests.utils import DatabaseTableFactory

@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class TestUploadFileSerializer(TestCase):
    def setUp(self):
        data = b'col1,col2\nval1,val2'
        self.content_file = SimpleUploadedFile("test.csv", data)
        self.table = DatabaseTableFactory.create()


    def test_validate_file_size(self):
        pass

    def test_save(self):
        data = {
            'name': 'test.csv',
            'file': self.content_file,
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
        serializer = serializers.UploadFileSerializer(data=data)

        request = Mock()
        request.parser_context = {'kwargs': {'pk': self.table.pk}}
        request.FILES = {'file': self.content_file}
        serializer._context = {'request': request}

        serializer.is_valid(raise_exception=True)

        with patch('dbtables.api.serializers.tasks.create_csv_file_from_data') as mcreate_csv:
            document = serializer.save()
            self.assertIsNotNone(document)
