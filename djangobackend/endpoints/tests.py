from django.test import TestCase
from django.urls import reverse


class TestPublicApiEndpoints(TestCase):
    fixtures = ['endpoints', 'fixtures/databases']

    def test_get_database_level_endpoint(self):
        path = reverse('endpoints:database-level-endpoint', kwargs={
            'endpoint': 'test-public-endpoint',
            'database': 'test-database'
        })

        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)


    def test_get_table_level_endpoint(self):
        path = reverse('endpoints:table-level-endpoint', kwargs={
            'endpoint': 'test-public-endpoint',
            'database': 'test-database',
            'table': 'test-table'
        })

        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)

    def test_post_table_level_endpoint(self):
        path = reverse('endpoints:table-level-endpoint', kwargs={
            'endpoint': 'test-public-endpoint',
            'database': 'test-database',
            'table': 'test-table'
        })

        response = self.client.post(path, data={})
        self.assertEqual(response.status_code, 200)

    def test_post_table_level_endpoint_with_data(self):
        path = reverse('endpoints:table-level-endpoint', kwargs={
            'endpoint': 'test-public-endpoint',
            'database': 'test-database',
            'table': 'test-table'
        })

        response = self.client.post(path, data={
            'key': 'value'
        })
        self.assertEqual(response.status_code, 200)

    def test_put_table_level_endpoint(self):
        path = reverse('endpoints:table-level-endpoint', kwargs={
            'endpoint': 'test-public-endpoint',
            'database': 'test-database',
            'table': 'test-table'
        })

        response = self.client.put(path, data={})
        self.assertEqual(response.status_code, 200)

    def test_patch_table_level_endpoint(self):
        path = reverse('endpoints:table-level-endpoint', kwargs={
            'endpoint': 'test-public-endpoint',
            'database': 'test-database',
            'table': 'test-table'
        })

        response = self.client.patch(path, data={})
        self.assertEqual(response.status_code, 200)

    def test_delete_table_level_endpoint(self):
        path = reverse('endpoints:table-level-endpoint', kwargs={
            'endpoint': 'test-public-endpoint',
            'database': 'test-database',
            'table': 'test-table'
        })

        response = self.client.delete(path)
        self.assertEqual(response.status_code, 200)
