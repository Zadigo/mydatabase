import csv
import json
import pathlib

from datasources.models import DataSource
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TransactionTestCase
from django.urls import reverse


class TestDatasourceApi(TransactionTestCase):
    fixtures = ['fixtures/users', 'sources']

    @classmethod
    def setUpClass(cls):
        cls.csv_file = 'name,age\nkendall,25'
        cls.file_path = None

    def tearDown(self):
        if self.file_path is not None:
            self.file_path.unlink()

    @property
    def _first_source(self):
        return DataSource.objects.first()

    @property
    def _get_user(self):
        return get_user_model().objects.first()

    def _create_data_source(self):
        csv_content = b"name,age\nBob,30\nAlice,25"

        uploaded_file = SimpleUploadedFile(
            name='source_file.csv',
            content=csv_content,
            content_type='text/csv'
        )

        # Save to database
        instance = DataSource.objects.create(
            user=self._get_user,
            name='Names',
            csv_file=uploaded_file
        )
        return instance

    def _create_file(self):
        csv_data = [
            ['nom', 'prénom', 'statut'],
            ['paul', 'Louvin', 'Envoyé'],
            ['Pauline', 'Gaumont', 'Non envoyé']
        ]

        media = pathlib.Path(settings.MEDIA_ROOT)
        self.file_path: pathlib.Path = media.joinpath('source_file.csv')

        with open(self.file_path, mode='w', newline='\n') as f:
            writer = csv.writer(f)
            writer.writerows(csv_data)
        return True

    def test_list_sources(self):
        path = reverse('datasource_api:list')
        response = self.client.get(path)

        self.assertEqual(response.status_code, 200)

        for item in response.json():
            with self.subTest(item=item):
                self.assertIn('id', item)

    def test_upload_source(self):
        self._create_file()

        with open(self.file_path, mode='rb') as f:
            uploaded_file = SimpleUploadedFile(
                name='source_file.csv',
                content=f.read(),
                content_type='text/csv'
            )

            data = {
                'name': 'My source',
                'csv_file': uploaded_file,
                'endpoint_url': '',
                'endpoint_data_key': '',
                'columns_to_keep': []
            }

            path = reverse('datasource_api:upload')
            response = self.client.post(path, data=data)

            self.assertEqual(response.status_code, 200)
            self.assertIsNotNone(response.json()['csv_file'])

    def test_load_source(self):
        # Simulate CSV file
        instance = self._create_data_source()
        path = reverse('datasource_api:load', args=[instance.data_source_id])
        response = self.client.post(path, QUERY_STRING='sortby=name')

        self.assertEqual(response.status_code, 200)

    def test_update_column_data_types(self):
        instance = self._create_data_source()
        path = reverse(
            'datasource_api:column_data_types',
            args=[
                instance.data_source_id
            ]
        )

        data = [
            {
                'column': 'name',
                'column_type': 'Text'
            },
            {
                'column': 'age',
                'column_type': 'Number'
            }
        ]
        response = self.client.post(
            path, data=data, content_type='application/json')

        self.assertEqual(response.status_code, 200)

    def test_delete_data_source(self):
        pass

    def test_send_to_webhook(self):
        pass
