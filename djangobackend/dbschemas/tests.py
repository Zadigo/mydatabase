import json

from dbschemas.models import DatabaseSchema
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase


class TestDatabaseStructure(TestCase):
    """Tests for the DatabaseSchema model including
    properties that we created as well as the slug creation"""
    
    fixtures = ['fixtures/databases']

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
        print(instance.slug)
        self.assertIsNotNone(instance.slug)
        self.assertTrue(instance.slug.startswith('test-database-'))

        instance.name = 'Updated Database Name'
        instance.save()
        self.assertTrue(instance.slug.startswith('updated-database-name-'))


class TestApiDatabases(APITestCase):
    fixtures = ['fixtures/databases']

    def test_list_databases(self):
        path = reverse('dbschemas:list_databases')
        response = self.client.get(path)

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIsInstance(data, list)

        for item in data:
            with self.subTest(item=item):
                self.assertIn('name', item)
                self.assertIn('tables', item)

                for table in item['tables']:
                    with self.subTest(table=table):
                        self.assertIn('name', table)
                        self.assertIn('documents', table)

    def test_create_database(self):
        path = reverse('dbschemas:create_database')
        response = self.client.post(path, {'name': 'New Database'})

        self.assertEqual(response.status_code, 201)

        data = response.json()
        self.assertIsInstance(data, dict)

        self.assertIn('name', data)
        self.assertEqual(data['name'], 'New Database')

    def test_update_database(self):
        instance = DatabaseSchema.objects.first()
        path = reverse('dbschemas:retrieve_update_database',
                       args=[instance.pk])
        response = self.client.patch(path, {'name': 'Updated Database'})

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIsInstance(data, dict)

        self.assertIn('name', data)
        self.assertEqual(data['name'], 'Updated Database')

        self.assertEqual(response.status_code, 200)

    def test_delete_database(self):
        instance = DatabaseSchema.objects.first()
        self.assertIsNotNone(
            instance, "No DatabaseSchema instance found in fixtures")

        path = reverse('dbschemas:delete_database', args=[instance.pk])
        response = self.client.delete(path)

        self.assertEqual(response.status_code, 204)

    def test_restart_database(self):
        instance = DatabaseSchema.objects.first()
        self.assertIsNotNone(
            instance, "No DatabaseSchema instance found in fixtures")

        path = reverse('dbschemas:restart_database', args=[instance.pk])
        response = self.client.post(path)

        self.assertEqual(response.status_code, 204)
        self.assertFalse(instance.databasetable_set.all().exists())


class TestDatabaseRelationshipsApi(APITestCase):
    fixtures = ['fixtures/databases']

    def _get_database(self):
        instance = DatabaseSchema.objects.first()
        message = "No DatabaseSchema instance found in fixtures"
        self.assertIsNotNone(instance, message)
        return instance

    def test_create_relationships(self):
        instance = self._get_database()
        path = reverse(
            'dbschemas:retrieve_update_destroy_relationships',
            args=[instance.pk]
        )

        tables = instance.databasetable_set.all()
        self.assertGreater(tables.count(), 0)

        table1 = tables.first()
        table2 = tables.last()

        data = json.dumps({
            "from_table": table1.id,
            "to_table": table2.id,
            "field_definitions": {
                "left": "field_a",
                "right": "field_b"
            },
            "meta_definitions": "1-1"
        })

        response = self.client.post(
            path, data, content_type='application/json')
        self.assertEqual(response.status_code, 201, response.content)
        print(response.json())


class TestDatabaseEndpointsApi(APITestCase):
    fixtures = ['fixtures/databases']

    def test_get_database_endpoints(self):
        instance = DatabaseSchema.objects.first()
        self.assertIsNotNone(
            instance, "No DatabaseSchema instance found in fixtures")

        instance.endpoint_set.create(
            methods='GET,POST'
        )

        path = reverse('dbschemas:list_database_endpoints', args=[instance.pk])
        response = self.client.get(path)

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIsInstance(data, list)

        for item in data:
            with self.subTest(item=item):
                self.assertIn('id', item)
                self.assertIn('methods', item)
                self.assertIn('endpoint', item)
                self.assertIn('endpoint_uuid', item)
                self.assertIn('database_schema', item)
