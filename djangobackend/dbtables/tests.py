import csv
import json
import pathlib

from dbtables.models import DatabaseTable
from django.conf import settings
from django.core.files.base import ContentFile
from django.test import TransactionTestCase
from django.urls import reverse


class TestApiTables(TransactionTestCase):
    fixtures = ['fixtures/databases']

    def setUp(self):
        self.instance = DatabaseTable.objects.first()

    def test_get_table(self):
        path = reverse('database_tables:update_table', args=[self.instance.pk])
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200, response.content)

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
        self.assertEqual(response.status_code, 200, response.content)

        data = response.json()
        self.assertEqual(data['name'], 'Some simple name')

    def test_delete_table(self):
        path = reverse('database_tables:update_table', args=[self.instance.pk])
        response = self.client.delete(path)
        self.assertEqual(response.status_code, 204, response.content)

    def test_create_table(self):
        path = reverse('database_tables:create_table')

        data = {'name': 'Simple table', 'database': self.instance.id}
        response = self.client.post(
            path, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 201, response.content)

        data = response.json()
        self.assertIn('id', data)
        self.assertEqual(data['name'], 'Simple table')


class TestUploadApiTables(TransactionTestCase):
    fixtures = ['fixtures/databases']

    def setUp(self):
        self.table = DatabaseTable.objects.first()

        self.filename = 'test.csv'
        self.filepath = pathlib.Path(settings.MEDIA_ROOT) / self.filename
        with open(self.filepath, mode='w', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'age'])
            writer.writerow(['Alice', 30])
            writer.writerow(['Bob', 25])

    def tearDown(self):
        self.filepath.unlink(missing_ok=True)

    def test_upload_file_via_csv(self):
        path = reverse('database_tables:upload_document', args=[self.table.pk])
        with open(self.filepath, mode='rb') as f:
            response = self.client.post(path, data={'file': f})
        self.assertEqual(response.status_code, 201, response.content)

    def test_upload_file_via_url(self):
        path = reverse('database_tables:upload_document', args=[self.table.pk])
        url = 'https://data.opendatasoft.com/api/explore/v2.1/catalog/datasets/panneaux4x3-feuille1@issy-les-moulineaux/records?limit=5'
        response = self.client.post(path, data={'url': url})
        self.assertEqual(response.status_code, 201, response.content)

    def test_upload_file_via_google_sheet_id(self):
        pass
