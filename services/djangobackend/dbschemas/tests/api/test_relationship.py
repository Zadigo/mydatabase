import json

from django.urls import reverse
from rest_framework.test import APITestCase

from dbschemas.models import DatabaseSchema


class TestDatabaseRelationshipsApi(APITestCase):
    fixtures = ('fixtures/databases',)

    def _get_database(self):
        instance = DatabaseSchema.objects.first()
        message = "No DatabaseSchema instance found in fixtures"
        self.assertIsNotNone(instance, message)
        return instance

    def test_create_relationships(self):
        instance = self._get_database()
        path = reverse(
            'dbschemas:retrieve_update_destroy_relationships',
            args=[instance.pk]
        )

        tables = instance.databasetable_set.all()
        self.assertGreater(tables.count(), 0)

        table1 = tables.first()
        table2 = tables.last()

        data = json.dumps({
            "from_table": table1.id,
            "to_table": table2.id,
            "field_definitions": {
                "left": "field_a",
                "right": "field_b"
            },
            "meta_definitions": "1-1"
        })

        response = self.client.post(
            path, data, content_type='application/json')
        self.assertEqual(response.status_code, 201, response.content)
        self.assertIn('tables', response.json())
        self.assertIn('document_relationships', response.json())
