from django.core.files.base import ContentFile
from django.test import TestCase, override_settings
from tabledocuments import tasks
from tabledocuments.models import TableDocument
from tabledocuments.tests.utils import DocumentFactory, create_file_based_instance
from tabledocuments.validation_models import ColumnOption


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


@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class TestTasks(TestCase):

    def test_get_document_from_url(self):
        t = tasks.get_document_from_url.apply(
            args=['https://jsonplaceholder.typicode.com/todos/1']
        )
        result = t.get()

    def test_append_to_dataframe(self):
        document: TableDocument = DocumentFactory.create()
        document.file.save(
            'test.csv',
            ContentFile('name,age\nAlice,30\nBob,25')
        )
        document.save()

        t = tasks.append_to_dataframe.apply(
            args=[
                document.document_uuid,
                'name,age\nCharlie,35'
            ]
        )

        t.get()

        document.file.delete()

    def test_get_document_from_google_sheet(self):
        pass

    def test_get_document_from_public_google_sheet(self):
        pass

    def test_create_csv_file_from_data(self):
        d1: TableDocument = DocumentFactory.create()

        # Test with bytes
        t = tasks.create_csv_file_from_data.apply(
            args=[
                b'name,age\nAlice,30\nBob,25',
                d1.document_uuid,
            ]
        )
        t.get()
        self.assertIsNotNone(d1.file)

        # # Test with string
        # d2 = DocumentFactory.create()
        # t = tasks.create_csv_file_from_data.apply(
        #     args=[
        #         'name,age\nAlice,30\nBob,25',
        #         d2.document_uuid,
        #     ]
        # )

        # t.get()
        # self.assertIsNotNone(d2.file)

        # # Test dict without entry key
        # # with self.assertLogs('tabledocuments.tasks', level='ERROR') as cm:
        # #     t = tasks.create_csv_file_from_data.apply(
        # #         args=[
        # #             {'name': 'Alice', 'age': 30},
        # #             d4.document_uuid,
        # #         ]
        # #     )
        # #     t.get()

        # # Test dict with entry key
        # d3 = DocumentFactory.create()
        # t = tasks.create_csv_file_from_data.apply(
        #     args=[
        #         {'items': [{'name': 'Alice', 'age': 30},
        #                    {'name': 'Bob', 'age': 25}]},
        #         d3.document_uuid,
        #         'items'
        #     ]
        # )
        # t.get()
        # print(d3.file)
        # self.assertIsNotNone(d3)
