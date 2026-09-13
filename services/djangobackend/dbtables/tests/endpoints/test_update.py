import pytest
from django.test import TransactionTestCase
from django.urls import reverse
from rest_framework.test import APIClient

from dbtables.models import DatabaseTable


@pytest.mark.api
class TestTablesUpdate(TransactionTestCase):
    fixtures = ('fixtures/databases',)

    def setUp(self):
        # self.databae = DatabaseSchemaFactory.create()
        self.instance = DatabaseTable.objects.first()

    def test_update_table(self):
        print(self.instance)
        path = reverse('database_tables:retrieve_update_delete_table', args=[self.instance.pk])
        data = {'name': 'Some simple name'}
        response = self.client.put(
            path, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200, response.content)

        data = response.json()
        self.assertEqual(data['name'], 'Some simple name')



UPDATE_DATA = pytest.mark.parametrize(
    "update_data",
    [
        {
            'expected_status': 200,
            'description': 'Update table name successfully',
            'data': {
                'name': 'Updated Table Name'
            }
        },
        # {
        #     'description': 'No database table with this id exists',
        #     'data': {
        #         'name': 'Updated Table Name'
        #     }
        # }
    ]
)

@pytest.mark.django_db
@UPDATE_DATA
def test_udpate_table_edge_cases(api_client: APIClient, table, update_data):
    path = reverse('database_tables:update_table', args=[table.pk])
    response = api_client.patch(path, data=update_data['data'], format='json')
    assert response.status_code == update_data['expected_status'], f"Response: {response.json()}"

    data = response.json()
    assert 'name' in data
    assert 'documents' in data
    assert data['name'] == update_data['data']['name']

