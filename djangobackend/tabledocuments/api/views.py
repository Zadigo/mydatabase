from rest_framework.generics import (DestroyAPIView,
                                     RetrieveUpdateDestroyAPIView)
from tabledocuments.api.serializer import SimpleDocumentSerializer
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

