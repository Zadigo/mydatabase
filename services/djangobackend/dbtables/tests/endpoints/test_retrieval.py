import pytest
from django.test import TransactionTestCase
from django.urls import reverse

from dbtables.models import DatabaseTable


@pytest.mark.api
class TestTablesRetrieval(TransactionTestCase):
    fixtures = ('fixtures/databases',)

    def setUp(self):
        self.instance = DatabaseTable.objects.first()

    def test_get_table(self):
        path = reverse('database_tables:retrieve_update_delete_table', args=[self.instance.pk])
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200, response.content)

        data = response.json()
        self.assertIn('name', data)
        self.assertIn('active_document_datasource', data)
