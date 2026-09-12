import pytest
from django.urls import reverse
from rest_framework.test import APIClient

CREATION_DATA = pytest.mark.parametrize(
    "creation_data",
    [
        {
            'name': 'Test Database',
        }
    ]
)


@pytest.mark.django_db
@CREATION_DATA
def test_create_database(api_client: APIClient, creation_data):
    path = reverse('dbschemas:create_database')
    response = api_client.post(path, data=creation_data)
    assert response.status_code == 201, f"Response: {response.json()}"
    assert 'name' in response.json()
