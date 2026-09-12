import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from dbschemas.models import DatabaseSchema
from dbtables.models import DatabaseTable


@pytest.mark.django_db
def test_restart_database(api_client: APIClient):
    instance = DatabaseSchema.objects.create(name='Test Database 1')
    DatabaseTable.objects.create(database_schema=instance)

    response = api_client.post(reverse('dbschemas:restart_database', kwargs={'pk': instance.pk}))
    assert response.status_code == 204
    assert instance.has_tables == False, "Database should have no tables after restart"
