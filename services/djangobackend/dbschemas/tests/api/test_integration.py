import json

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework.test import APITestCase

from dbschemas.models import DatabaseSchema


class TestCreateIntegrationApi(APITestCase):
    fixtures = ('fixtures/databases',)

    def _get_database(self):
        instance = DatabaseSchema.objects.first()
        message = "No DatabaseSchema instance found in fixtures"
        self.assertIsNotNone(instance, message)
        return instance

    def test_create_integration_no_data(self):
        instance = self._get_database()
        path = reverse('dbschemas:create_integration', args=[instance.pk])

        response = self.client.post(path, {}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': True})

    def test_create_integration_google_sheets_invalid(self):
        instance = self._get_database()
        path = reverse('dbschemas:create_integration', args=[instance.pk])

        data = {'google_sheets': 'invalid-data'}

        response = self.client.post(path, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('google_sheets', response.json())

    def test_create_integration_google_sheets_valid(self):
        instance = self._get_database()
        path = reverse('dbschemas:create_integration', args=[instance.pk])

        valid_json_content = json.dumps({
            "type": "fake_account",
            "project_id": "django_fake_id",
            "private_key_id": "fake-123",
            "private_key": "begin-is-fake-end",
            "client_email": "fake@example.com",
            "client_id": "123",
            "auth_uri": "https://accounts.example.com/o/oauth2/auth",
            "token_uri": "https://oauth2.example.com/token",
            "auth_provider_x509_cert_url": "https://www.example.com/oauth2/v1/certs",
            "client_x509_cert_url": "http://iam.example.com",
            "universe_domain": "exampleapis.com"
        })

        file = SimpleUploadedFile(
            "valid_credentials.json",
            valid_json_content.encode()
        )

        data = {'google_sheets': file}

        response = self.client.post(path, data)
        self.assertEqual(response.status_code, 201, response.content)
        self.assertIn('has_google_sheet_connection', response.json())
        self.assertTrue(response.json()['has_google_sheet_connection'])
