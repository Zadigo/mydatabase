import pytest
from django.urls import reverse

from djangobackend.utils import authenticated_client
from tabledocuments.tests.utils import DocumentFactory
from tabledocuments.validation_models import (
    ColumnOptionsModel,
    OptionalColumnOptionsModel,
)


@pytest.fixture
def document():
    return DocumentFactory.create()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "name,options",
    [
        ("No options", []),
        ("With options", [ColumnOptionsModel(name="firstname").model_dump()]),
    ]
)
def test_update_document(name, options):
    document = DocumentFactory.create()

    path = reverse(
        'documents:retrieve_update_destroy_document',
        args=[
            document.document_uuid
        ]
    )
    client = authenticated_client()
    response = client.patch(
        path, 
        data={
            'name': name,
            'column_options': options
        }, 
        content_type='application/json'
    )
    
    assert response.status_code == 200, response.content



@pytest.mark.django_db
def test_update_column_types(document):
    path = reverse('documents:update_column_types', args=[document.pk])
    client = authenticated_client()
    response = client.patch(
        path, 
        data=OptionalColumnOptionsModel().model_dump(),
        content_type='application/json'
    )
    
    assert response.status_code == 200, response.content
