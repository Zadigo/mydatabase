import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from dbschemas.models import DatabaseSchema


@pytest.mark.django_db
def test_retrieve_update(api_client: APIClient):
    instance = DatabaseSchema.objects.create(name='Test Database 1')
    response = api_client.get(reverse('dbschemas:retrieve_update_database', kwargs={'pk': instance.pk}))
    assert response.status_code == 200, f"Response: {response.json()}"

    update_data = {'name': 'Updated Database'}
    response = api_client.put(reverse('dbschemas:retrieve_update_database', kwargs={'pk': instance.pk}), data=update_data)
    assert response.status_code == 200, f"Response: {response.json()}"

    # Try to retrieve a non-existent database
    response = api_client.get(reverse('dbschemas:retrieve_update_database', kwargs={'pk': 99}))
    assert response.status_code == 404, f"Response: {response.json()}"


@pytest.mark.django_db
def test_list_databases(api_client: APIClient):
    response = api_client.get(reverse('dbschemas:list_databases'))
    assert response.status_code == 200

    DatabaseSchema.objects.create(name='Test Database 1')
    response = api_client.get(reverse('dbschemas:list_databases'))
    assert response.status_code == 200
    assert len(response.json()) == 1

    data = response.json()[0]
    assert 'name' in data
    

CREATION_DATA = pytest.mark.parametrize(
    "creation_data",
    [
        {
            'name': 'Test Database',
        }
    ]
)

