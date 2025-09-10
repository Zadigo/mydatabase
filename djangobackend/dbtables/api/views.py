from dbtables.api.serializers import (DatabaseTableSerializer,
                                      UploadFileSerializer)
from dbtables.models import DatabaseTable
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView


class UpdateTable(RetrieveUpdateDestroyAPIView):
    """Endpoint used to update metadata for a 
    database table."""

    queryset = DatabaseTable.objects.all()
    serializer_class = DatabaseTableSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'
    permission_classes = []


class UploadNewDocument(CreateAPIView):
    """Endpoint used to upload a new file as a document
    or either via an url. The file is parsed and stored
    in the database."""

    queryset = DatabaseTable.objects.all()
    serializer_class = UploadFileSerializer
    permission_classes = []


class CreateTable(CreateAPIView):
    """Endpoint used to create a new database table."""

    queryset = DatabaseTable.objects.all()
    serializer_class = DatabaseTableSerializer
    permission_classes = []
