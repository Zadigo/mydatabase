import json

from dbtables.models import DatabaseTable
from django.test import TransactionTestCase
from django.urls import reverse


class TestApiTables(TransactionTestCase):
    fixtures = ['fixtures/databases']

    def setUp(self):
        self.instance = DatabaseTable.objects.first()

    def test_get_table(self):
        path = reverse('database_tables:update_table', args=[self.instance.pk])
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn('name', data)
        self.assertIn('active_document_datasource', data)

    def test_update_table(self):
        path = reverse('database_tables:update_table', args=[self.instance.pk])
        data = json.dumps({
            'name': 'Some simple name'
        })
        response = self.client.put(
            path, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data['name'], 'Some simple name')

    def test_delete_table(self):
        path = reverse('database_tables:update_table', args=[self.instance.pk])
        response = self.client.delete(path)
        self.assertEqual(response.status_code, 204)
