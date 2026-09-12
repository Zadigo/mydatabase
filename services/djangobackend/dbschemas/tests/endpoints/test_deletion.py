import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from dbschemas.models import DatabaseSchema


@pytest.mark.django_db
def test_delete_database(api_client: APIClient):
    instance = DatabaseSchema.objects.create(name='Test Database 1')
    response = api_client.delete(reverse('dbschemas:delete_database', kwargs={'pk': instance.pk}))
    assert response.status_code == 204, f"Response: {response.json()}"

    response = api_client.delete(reverse('dbschemas:delete_database', kwargs={'pk': 99}))
    assert response.status_code == 404, f"Response: {response.json()}"
