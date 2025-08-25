from dbschemas.models import DatabaseSchema
from django.urls import reverse
from rest_framework.test import APITestCase


class TestListDatabases(APITestCase):
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

    def test_delete_database(self):
        instance = DatabaseSchema.objects.first()
        self.assertIsNotNone(
            instance, "No DatabaseSchema instance found in fixtures")

        path = reverse('dbschemas:delete_database', args=[instance.pk])
        response = self.client.delete(path)

        self.assertEqual(response.status_code, 204)
