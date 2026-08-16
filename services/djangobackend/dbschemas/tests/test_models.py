import unittest

import pytest

from dbschemas.models import DatabaseProvider, DatabaseSchema


@pytest.mark.django_db
class TestDatabaseSchemaModel(unittest.TestCase):
    def setUp(self):
        self.schema = DatabaseSchema.objects.create(name="Test Schema")

    def test_has_relationships_property(self):
        self.assertFalse(self.schema.has_relationships)

    def test_has_triggers(self):
        self.assertFalse(self.schema.has_triggers)

    def test_has_functions(self):
        self.assertFalse(self.schema.has_functions)

    def test_table_count(self):
        self.assertTrue(self.schema.table_count == 0)

    def test_has_tables(self):
        self.assertFalse(self.schema.has_tables)


@pytest.mark.django_db
class TestDatabaseProviderModel(unittest.TestCase):
    def setUp(self):
        schema = DatabaseSchema.objects.create(name="Test Schema")
        self.provider = DatabaseProvider.objects.create(database_schema=schema)

    def test_has_google_sheet_connection(self):
        self.assertFalse(self.provider.has_google_sheet_connection)
