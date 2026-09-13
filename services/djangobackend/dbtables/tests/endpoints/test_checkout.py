import pytest
from django.urls import reverse

from dbschemas.models import DatabaseSchema
from dbtables.models import DatabaseTable
from tabledocuments.models import TableDocument


@pytest.fixture
def urlpath():
    instance: TableDocument = TableDocument.objects.create(name='test.csv')
    schema = DatabaseSchema.objects.create(name='test_schema')
    db = DatabaseTable.objects.create(name='test_table', database_schema=schema)

    return reverse(
        'database_tables:checkout_document',
        args=[instance.pk]
    )


@pytest.mark.django_db
def test_checkout_document(urlpath, api_client, csv_django_file):
    assert urlpath is not None
    response = api_client.post(
        urlpath, 
        data={
            'url': '',
            'file': csv_django_file
        }
    )
    assert response.status_code == 201
    assert 'sample' in response.data
    assert 'numberOfRows' in response.data
    assert 'numberOfColumns' in response.data
    assert 'columns' in response.data
    assert 'columnTypes' in response.data
    