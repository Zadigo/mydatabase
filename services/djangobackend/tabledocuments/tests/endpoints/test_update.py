import pytest
from django.urls import reverse

from djangobackend.utils import authenticated_client
from tabledocuments.tests.utils import DocumentFactory


@pytest.mark.django_db
def test_update_document():
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
            'name': 'Updated Document Name'
        }, 
        content_type='application/json'
    )
    
    assert response.status_code == 200, response.content
