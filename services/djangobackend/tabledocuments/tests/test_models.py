from django.test import TestCase

from tabledocuments.models import TableDocument
from tabledocuments.tests.utils import DocumentFactory, create_file_based_instance
from tabledocuments.validation_models import ColumnOptionsModel, ColumnTypeOptionsModel


class TestTableDocument(TestCase):
    def test_model_creation(self):
        instance = create_file_based_instance()
        self.assertIsNotNone(instance.file, instance.file)
        instance.file.delete(save=True)

    def test_mixed_options(self):
        instance: TableDocument = DocumentFactory.create()

        options = ColumnOptionsModel(name='firstname')
        instance.column_options = [options.model_dump()]
        
        type_options = ColumnTypeOptionsModel(name='firstname')
        instance.column_types = [type_options.model_dump()]

        instance.save()

        self.assertIsNotNone(instance.column_options)
        self.assertIsNotNone(instance.column_types)
