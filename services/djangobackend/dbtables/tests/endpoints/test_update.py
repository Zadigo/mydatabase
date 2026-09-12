from django.test import TransactionTestCase
from django.urls import reverse

from dbtables.models import DatabaseTable


class TestTablesUpdate(TransactionTestCase):
    fixtures = ('fixtures/databases',)

    def setUp(self):
        # self.databae = DatabaseSchemaFactory.create()
        self.instance = DatabaseTable.objects.first()

    def test_update_table(self):
        print(self.instance)
        path = reverse('database_tables:update_table', args=[self.instance.pk])
        data = {'name': 'Some simple name'}
        response = self.client.put(
            path, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200, response.content)

        data = response.json()
        self.assertEqual(data['name'], 'Some simple name')
