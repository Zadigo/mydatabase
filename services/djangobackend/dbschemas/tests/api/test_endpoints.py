
from django.urls import reverse
from rest_framework.test import APITestCase

from dbschemas.models import DatabaseSchema


class TestDatabaseEndpointsApi(APITestCase):
    fixtures = ('fixtures/databases',)

    def test_get_database_endpoints(self):
        instance = DatabaseSchema.objects.first()
        self.assertIsNotNone(
            instance, "No DatabaseSchema instance found in fixtures")

        instance.publicapiendpoint_set.create(methods=['GET', 'POST'])

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
