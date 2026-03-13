from django.test import TestCase

from tabledocuments.models import TableDocument
from tabledocuments.tests.utils import create_file_based_instance, DocumentFactory
from tabledocuments.validation_models import ColumnOption, ColumnTypeOption

class TestTableDocument(TestCase):
    def test_model_creation(self):
        instance = create_file_based_instance()
        self.assertIsNotNone(instance.file, instance.file)
        instance.file.delete(save=True)

    def test_mixed_options(self):
        instance: TableDocument = DocumentFactory.create()

        options = ColumnOption(name='firstname')
        instance.column_options = [options.model_dump()]
        
        type_options = ColumnTypeOption(name='firstname')
        instance.column_types = [type_options.model_dump()]

        instance.save()

        self.assertIn('unique', instance.mixed_options)
        self.assertIn('name', instance.mixed_options)
