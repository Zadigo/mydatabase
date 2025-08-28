from django.urls import re_path
from tabledocuments.api import views

app_name = 'documents'

urlpatterns = [
    re_path(
        r'^(?P<document_uuid>[a-z0-9\-]+)$',
        views.RetrieveUpdateDestroyDocument.as_view(),
        name='retrieve_update_destroy_document'
    )
]
