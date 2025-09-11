from typing import Generic, TypeVar
from django.shortcuts import get_object_or_404
from dbschemas.api.serializers import DatabaseSchemaSerializer
from dbschemas.models import DatabaseSchema
from endpoints.api.serializers import PublicApiEndpointSerializer
from rest_framework import status
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     GenericAPIView, ListAPIView,
                                     RetrieveUpdateAPIView)
from rest_framework.response import Response

T = TypeVar('T', bound=GenericAPIView)

class QuerysetMixin(Generic[T]):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)


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


class UpdateDatabase(RetrieveUpdateAPIView):
    queryset = DatabaseSchema.objects.all()
    serializer_class = DatabaseSchemaSerializer
    permission_classes = []


class RestartProject(GenericAPIView):
    """Endpoint that deletes all the data contained in the
    documents provided by the tables and recursively deletes
    the tables and documents associated with this database"""

    queryset = DatabaseSchema.objects.all()
    permission_classes = []

    def post(self, request, *args, **kwargs):
        obj = super().get_object()
        tables = obj.databasetable_set.all()

        for table in tables:
            documents = table.documents.all()

            for document in documents:
                document.delete()
            
            table.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ListDatabaseEndpoints(ListAPIView):
    """List all public API endpoints associated with a 
    specific database schema."""

    queryset = DatabaseSchema.objects.all()
    serializer_class = PublicApiEndpointSerializer
    permission_classes = []

    def get_queryset(self):
        qs = super().get_queryset()
        database = get_object_or_404(qs, pk=self.kwargs['pk'])
        return database.publicapiendpoint_set.all()
