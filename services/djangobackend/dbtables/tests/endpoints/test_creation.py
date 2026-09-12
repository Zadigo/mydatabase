from django.test import TransactionTestCase
from django.urls import reverse

from dbtables.models import DatabaseTable


class TestTablesCreation(TransactionTestCase):
    fixtures = ('fixtures/databases',)

    def setUp(self):
        self.instance = DatabaseTable.objects.first()

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
