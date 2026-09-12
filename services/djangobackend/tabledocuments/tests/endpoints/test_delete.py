import pytest
from django.urls import reverse

from djangobackend.utils import authenticated_client
from tabledocuments.tests.utils import DocumentFactory


@pytest.mark.django_db
def test_delete_document():
    client = authenticated_client()
    document = DocumentFactory.create()
    
    path = reverse(
        'documents:retrieve_update_destroy_document', 
        args=[
            document.document_uuid
        ]
    )
    response = client.delete(path)
    assert response.status_code == 204, response.content
