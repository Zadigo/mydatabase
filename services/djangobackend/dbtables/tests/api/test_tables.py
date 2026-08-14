from django.test import TransactionTestCase
from django.urls import reverse

from dbtables.models import DatabaseTable


class TestApiTables(TransactionTestCase):
    fixtures = ('fixtures/databases',)

    def setUp(self):
        # self.databae = DatabaseSchemaFactory.create()
        self.instance = DatabaseTable.objects.first()

    def test_get_table(self):
        path = reverse('database_tables:update_table', args=[self.instance.pk])
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200, response.content)

        data = response.json()
        self.assertIn('name', data)
        self.assertIn('active_document_datasource', data)

    def test_update_table(self):
        print(self.instance)
        path = reverse('database_tables:update_table', args=[self.instance.pk])
        data = {'name': 'Some simple name'}
        response = self.client.put(
            path, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200, response.content)

        data = response.json()
        self.assertEqual(data['name'], 'Some simple name')

    def test_delete_table(self):
        path = reverse('database_tables:update_table', args=[self.instance.pk])
        response = self.client.delete(path)
        self.assertEqual(response.status_code, 204, response.content)

    def test_create_table(self):
        path = reverse('database_tables:create_table')

        data = {'name': 'Simple table', 'database': self.instance.id}
        response = self.client.post(
            path, data=data, content_type='application/json'
        )
        self.assertEqual(response.status_code, 201, response.content)

        data = response.json()
        self.assertIn('id', data)
        self.assertEqual(data['name'], 'Simple table')
