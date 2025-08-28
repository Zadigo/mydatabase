from rest_framework.generics import (DestroyAPIView,
                                     RetrieveUpdateDestroyAPIView)
from tabledocuments.api.serializer import SimpleDocumentSerializer
from tabledocuments.models import TableDocument


class GetDocument(RetrieveUpdateDestroyAPIView):
    """Returns simple information about the given
    document (without the data it contains)"""

    queryset = TableDocument.objects.all()
    serializer_class = SimpleDocumentSerializer
    permission_classes = []


class DeleteDocumentView(DestroyAPIView):
    """View to handle document deletion requests"""

    queryset = TableDocument.objects.all()
    lookup_field = 'document_uuid'
    lookup_url_kwarg = 'document_uuid'
    permission_classes = []
