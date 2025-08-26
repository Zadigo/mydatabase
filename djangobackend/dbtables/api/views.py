from dbtables.api.serializers import DatabaseTableSerializer
from dbtables.models import DatabaseTable
from rest_framework.generics import RetrieveUpdateDestroyAPIView


class UpdateTable(RetrieveUpdateDestroyAPIView):
    """Endpoint used to update metadata for a 
    database table."""

    queryset = DatabaseTable.objects.all()
    serializer_class = DatabaseTableSerializer
    permission_classes = []
