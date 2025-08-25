from dbschemas.api.serializers import DatabaseSchemaSerializer
from dbschemas.models import DatabaseSchema
from rest_framework.generics import ListAPIView


class ListDatabases(ListAPIView):
    queryset = DatabaseSchema.objects.all()
    serializer_class = DatabaseSchemaSerializer
    permission_classes = []
