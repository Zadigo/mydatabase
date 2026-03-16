from unittest.mock import patch

from django.core.files.base import ContentFile
from django.test import TestCase, override_settings
from tabledocuments import tasks
from tabledocuments.models import TableDocument
from tabledocuments.tests.utils import DocumentFactory, build_column_options, create_file_based_instance
from tabledocuments.validation_models import ColumnOption



@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class TestCreateCsvFileFromData(TestCase):
    def test_create_from_bytes(self):
        instance: TableDocument = DocumentFactory.create()

        with patch('tabledocuments.tasks.update_document_options') as mupdate_options:
            result = tasks.create_csv_file_from_data.apply(kwargs={
                'data': b'firstname,lastname\nJane,Doe',
                'document_id': instance.id,
                'column_options': build_column_options('firstname', 'lastname')
            })
            result.get()

            instance.refresh_from_db()
            self.assertIsNotNone(instance.file)

            instance.file.delete()

    def test_create_from_string(self):
        instance: TableDocument = DocumentFactory.create()

        with patch('tabledocuments.tasks.update_document_options') as mupdate_options:
            result = tasks.create_csv_file_from_data.apply(kwargs={
                'data': 'firstname,lastname\nJane,Doe',
                'document_id': instance.id,
                'column_options': build_column_options('firstname', 'lastname')
            })
            result.get()

            instance.refresh_from_db()
            self.assertIsNotNone(instance.file)

            instance.file.delete()


@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class TestCreateJsonFileFromData(TestCase):
    def test_create_from_dict(self):
        instance: TableDocument = DocumentFactory.create()

        with patch('tabledocuments.tasks.update_document_options') as mupdate_options:
            result = tasks.create_json_file_from_data.apply(kwargs={
                'data': {'items': [{'firstname': 'Jane', 'lastname': 'Doe'}]},
                'document_id': instance.id,
                'column_options': build_column_options('firstname', 'lastname'),
                'entry_key': 'items'
            })
            result.get()

            instance.refresh_from_db()
            self.assertIsNotNone(instance.file)

            instance.file.delete()

    def test_create_from_dict_without_entry_key(self):
        instance: TableDocument = DocumentFactory.create()

        result = tasks.create_json_file_from_data.apply(kwargs={
            'data': {'firstname': 'Jane', 'lastname': 'Doe'},
            'document_id': instance.id,
            'column_options': build_column_options('firstname', 'lastname')
        })
        
        result.get()

        instance.refresh_from_db()
        self.assertIsNotNone(instance.file)

    def test_create_from_list(self):
        instance: TableDocument = DocumentFactory.create()

        with patch('tabledocuments.tasks.update_document_options') as mupdate_options:
            result = tasks.create_json_file_from_data.apply(kwargs={
                'data': [{'firstname': 'Jane', 'lastname': 'Doe'}],
                'document_id': instance.id,
                'column_options': build_column_options('firstname', 'lastname')
            })
            result.get()

            instance.refresh_from_db()
            self.assertIsNotNone(instance.file)

            instance.file.delete()


@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class TestCreateFeatherFileFromData(TestCase):
    pass


@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class TestCreateFileFromData(TestCase):
    def setUp(self):
        self.instance: TableDocument = DocumentFactory.create()

    def test_invalid_document(self):
        pass



@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class TestGetDocumentFromUrl(TestCase):
    def test_base_retrieval(self):
        with patch('tabledocuments.tasks.update_document_options') as mupdate_options:
            url = 'https://jsonplaceholder.typicode.com/todos'
            t = tasks.get_document_from_url.apply(args=[url])
            t.get()

    def test_retrieval_from_a_dict_should_fail(self):
        with patch('tabledocuments.tasks.update_document_options') as mupdate_options:
            url = 'https://jsonplaceholder.typicode.com/todos/1'
            t = tasks.get_document_from_url.apply(args=[url])
            t.get()
            

@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class TestAppendToDataframe(TestCase):
    def test_append_with_strings(self):
        instance: TableDocument = DocumentFactory.create()

        str_data = b'firstname,lastname\nJane,Doe'
        content_file = ContentFile(str_data, name='test.csv')
        instance.file.save('test.csv', content_file)

        data_to_append = b'firstname,lastname\nJohn,Smith'
        t = tasks.append_to_dataframe.apply(args=[instance.document_uuid, data_to_append])
        t.get()


@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class TestUpdateDocumentOptions(TestCase):
    def setUp(self):
        column_options = [
            ColumnOption(
                name='name',
                visible=True,
                editable=True,
                sortable=True,
                searchable=True
            )
        ]

        column_options = list(map(lambda x: x.model_dump(), column_options))

        instance = create_file_based_instance()
        instance.column_options = column_options
        instance.save()

        self.instance = instance

    def test_document_not_found(self):
        pass

    def test_from_file(self):
        result = tasks.update_document_options.apply(
            args=[
                self.instance.document_uuid, 
                self.instance.column_options
            ]
        )
        result.get()

        self.instance.refresh_from_db()
        self.assertDictEqual(self.instance.column_types, {'name': 'String'})
