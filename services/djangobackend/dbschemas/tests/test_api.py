from django.test import TestCase

from dbschemas.models import DatabaseSchema


class TestDatabaseStructure(TestCase):
    """Tests for the DatabaseSchema model including
    properties that we created as well as the slug creation"""

    fixtures = ('fixtures/databases',)

    def test_optional_properties(self):
        instance = DatabaseSchema.objects.first()
        self.assertFalse(instance.has_relationships)
        self.assertFalse(instance.has_triggers)
        self.assertFalse(instance.has_functions)

    def test_has_tables(self):
        instance = DatabaseSchema.objects.first()
        self.assertTrue(instance.has_tables)

    def test_slug_creation(self):
        instance = DatabaseSchema.objects.create(name='Test Database')

        self.assertIsNotNone(instance.slug)
        self.assertTrue(instance.slug.startswith('test-database-'))

        instance.name = 'Updated Database Name'
        instance.save()
        self.assertTrue(instance.slug.startswith('updated-database-name-'))
