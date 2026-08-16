import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from dbschemas.models import DatabaseSchema
from dbtables.models import DatabaseTable


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


@pytest.mark.django_db
@CREATION_DATA
def test_create_database(api_client: APIClient, creation_data):
    response = api_client.post(reverse('dbschemas:create_database'), data=creation_data)
    assert response.status_code == 201, f"Response: {response.json()}"


@pytest.mark.django_db
def test_delete_database(api_client: APIClient):
    instance = DatabaseSchema.objects.create(name='Test Database 1')
    response = api_client.delete(reverse('dbschemas:delete_database', kwargs={'pk': instance.pk}))
    assert response.status_code == 204, f"Response: {response.json()}"

    response = api_client.delete(reverse('dbschemas:delete_database', kwargs={'pk': 99}))
    assert response.status_code == 404, f"Response: {response.json()}"


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
def test_restart_database(api_client: APIClient):
    instance = DatabaseSchema.objects.create(name='Test Database 1')
    DatabaseTable.objects.create(database_schema=instance)

    response = api_client.post(reverse('dbschemas:restart_database', kwargs={'pk': instance.pk}))
    assert response.status_code == 204
    assert instance.has_tables == False, "Database should have no tables after restart"
