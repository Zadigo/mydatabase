from django.urls import reverse
from rest_framework.test import APITestCase


class TestListDatabses(APITestCase):
    fixtures = []
    
    def test_list_databases(self):
        path = reverse('dbschemas:list_databases')
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
