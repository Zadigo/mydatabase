from dbtables.api.serializers import DatabaseTableSerializer, UploadFileSerializer
from dbtables.models import DatabaseTable
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView


class UpdateTable(RetrieveUpdateDestroyAPIView):
    """Endpoint used to update metadata for a 
    database table."""

    queryset = DatabaseTable.objects.all()
    serializer_class = DatabaseTableSerializer
    permission_classes = []



class UploadNewDocument(CreateAPIView):
    """Endpoint used to upload a new file either
    directly or via an url"""

    queryset = DatabaseTable.objects.all()
    serializer_class = UploadFileSerializer
    permission_classes = []


class CreateTable(CreateAPIView):
    """Endpoint used to update metadata for a 
    database table."""

    queryset = DatabaseTable.objects.all()
    serializer_class = DatabaseTableSerializer
    permission_classes = []
