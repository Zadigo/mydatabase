import pytest
from django.urls import reverse

from djangobackend.utils import authenticated_client
from tabledocuments.tests.utils import DocumentFactory


@pytest.mark.django_db
def test_get_document():
    document = DocumentFactory.create()
    
    client = authenticated_client()
    path = reverse(
        'documents:retrieve_update_destroy_document', 
        args=[
            document.document_uuid
        ]
    )
    response = client.get(path)
    assert response.status_code == 200, response.content
    assert isinstance(response.json(), dict)

