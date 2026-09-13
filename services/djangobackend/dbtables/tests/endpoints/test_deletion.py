import pytest
from django.test import TransactionTestCase
from django.urls import reverse

from dbtables.models import DatabaseTable


@pytest.mark.api
class TestTableDeletion(TransactionTestCase):
    fixtures = ('fixtures/databases',)

    def setUp(self):
        self.instance = DatabaseTable.objects.first()

    def test_delete_table(self):
        path = reverse('database_tables:retrieve_update_delete_table', args=[self.instance.pk])
        response = self.client.delete(path)
        self.assertEqual(response.status_code, 204, response.content)
