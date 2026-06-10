from django.test import TestCase
from django.urls import reverse
from dbtables.models import DatabaseTable
from tabledocuments.models import TableDocument
from tabledocuments.tests.utils import DocumentFactory
from dbtables.tests.utils import DatabaseTableFactory
from django.core.files.base import ContentFile
from endpoints.tests.utils import PublicApiEndpointFactory

class TestPublicApiEndpointRouter(TestCase):
    def setUp(self):
        self.table: DatabaseTable = DatabaseTableFactory.create()
        self.document: TableDocument  = DocumentFactory.create()
        self.table.active_document_datasource = self.document.document_uuid
        self.table.save()

        self.endpoint = PublicApiEndpointFactory.create(database_schema=self.table.database_schema)

        byte_content = b'name,age\nAlice,30\nBob,25'
        content_file = ContentFile(byte_content, name='test_document.csv')

        self.document.file.save('test_document.csv', content_file)
        self.document.save()

    def tearDown(self):
        self.document.file.delete()

    def test_get_valid_request(self):
        path = reverse(
            'endpoints:table_level_api_endpoint', 
            args=[
                self.table.database_schema.id, 
                self.table.id, 
                self.endpoint.endpoint_uuid
            ]
        )
        response = self.client.get(path, headers={
            'Authorization': f'Bearer {self.endpoint.bearer_token}'
        })
        self.assertEqual(response.status_code, 200, response.content)
        self.assertIn('data', response.json())
        self.assertIn('resource', response.json())
        self.assertIn('database', response.json())
        self.assertIn('table', response.json())

    def test_get_valid_request_with_select_query(self):
        path = reverse(
            'endpoints:table_level_api_endpoint', 
            args=[
                self.table.database_schema.id, 
                self.table.id, 
                self.endpoint.endpoint_uuid
            ]
        )
        response = self.client.get(
            path, 
            headers={
                'Authorization': f'Bearer {self.endpoint.bearer_token}'
            }, 
            data={
                'select': 'name'
            }
        )
        self.assertEqual(response.status_code, 200, response.content)
        print(response.json())

    def test_get_request_without_bearer_token(self):
        path = reverse(
            'endpoints:table_level_api_endpoint', 
            args=[
                self.table.database_schema.id, 
                self.table.id, 
                self.endpoint.endpoint_uuid
            ]
        )
        response = self.client.get(path)
        self.assertEqual(response.status_code, 400, response.content)
