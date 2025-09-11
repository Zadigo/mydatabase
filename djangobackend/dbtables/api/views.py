from dbtables.api.serializers import (DatabaseTableSerializer,
                                      UploadFileSerializer)
from dbtables.models import DatabaseTable
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from tabledocuments.api.serializer import SimpleDocumentSerializer
from rest_framework.permissions import IsAuthenticated


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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        response_serializer = SimpleDocumentSerializer(instance=serializer.instance)
        template = {'id': response_serializer.data.get('id'), 'document_uuid': response_serializer.data.get('document_uuid')}
        return Response(template, status=status.HTTP_201_CREATED, headers=headers)


class CreateTable(CreateAPIView):
    """Endpoint used to create a new database table."""

    queryset = DatabaseTable.objects.all()
    serializer_class = DatabaseTableSerializer
    permission_classes = []
