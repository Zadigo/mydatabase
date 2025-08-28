from django.urls import re_path
from tabledocuments.api import views

urlpatterns = [
    re_path(
        r'^(?P<document_uuid>[a-z0-9\-]+)$',
        views.DeleteDocumentView.as_view(),
        name='delete_document'
    )
]
