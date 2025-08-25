from dbschemas.api.serializers import DatabaseSchemaSerializer
from dbschemas.models import DatabaseSchema
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView


class ListDatabases(ListAPIView):
    queryset = DatabaseSchema.objects.all()
    serializer_class = DatabaseSchemaSerializer
    permission_classes = []



class CreateDatabase(CreateAPIView):
    serializer_class = DatabaseSchemaSerializer
    permission_classes = []


class DeleteDatabase(DestroyAPIView):
    queryset = DatabaseSchema.objects.all()
    serializer_class = DatabaseSchemaSerializer
    permission_classes = []
