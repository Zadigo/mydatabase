from django.test import TestCase

from tabledocuments.tests.utils import create_file_based_instance

class TestTableDocument(TestCase):
    def test_model_creation(self):
        instance = create_file_based_instance()
        self.assertIsNotNone(instance.file, instance.file)
        instance.file.delete(save=True)
