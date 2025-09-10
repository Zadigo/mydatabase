from rest_framework.generics import (DestroyAPIView, UpdateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from tabledocuments.api.serializer import SimpleDocumentSerializer, UpdateColumnTypesSerializer
from tabledocuments.models import TableDocument


class RetrieveUpdateDestroyDocument(RetrieveUpdateDestroyAPIView):
    """Returns simple information about the given
    document (without the data it contains) or deletes
    or updates part of it"""

    queryset = TableDocument.objects.all()
    serializer_class = SimpleDocumentSerializer
    lookup_field = 'document_uuid'
    lookup_url_kwarg = 'document_uuid'
    permission_classes = []



class UpdateColumnTypes(UpdateAPIView):
    """View to update the column types of a given document.
    Column types are a mapping of column names to their data types."""
    
    queryset = TableDocument.objects.all()
    serializer_class = UpdateColumnTypesSerializer
    permission_classes = []
