import json
from typing import Generic, TypeVar
from rest_framework import serializers
from dbschemas.api.serializers import (DatabaseSchemaSerializer,
                                       RelationshipSerializer,
                                       ValidateIntegrationSerializer, DatabaseProviderSerializer)
from dbschemas.models import DatabaseProvider, DatabaseSchema
from django.shortcuts import get_object_or_404
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


class RetrieveUpdateDestroyRelationships(GenericAPIView):
    """Endpoint used to retrieve, update or delete
    relationships for a database table."""

    queryset = DatabaseSchema.objects.all()
    serializer_class = RelationshipSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'
    permission_classes = []

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance=instance.database_schema.relationships, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        database_serializer = DatabaseSchemaSerializer(
            instance=serializer.instance)
        return Response(database_serializer.data, status=status.HTTP_201_CREATED)


class CreateIntegration(GenericAPIView):
    """Endpoint used to create integrations with external
    data providers like Airtable, Google Sheets, etc.
    """

    serializer_class = ValidateIntegrationSerializer
    response_serializer = DatabaseProviderSerializer

    def get_response_serializer(self, instance):
        serializer = self.response_serializer(instance=instance)
        data = serializer.data
        return data

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        google_sheets_file = request.FILES.get('google_sheets', None)
        if google_sheets_file:
            data = json.load(google_sheets_file)

            # Check the fields that are returned by the JSON file
            expected_fields = [
                'type', 'project_id', 'private_key_id',
                'private_key', 'client_email', 'client_id',
                'auth_uri', 'token_uri', 'auth_provider_x509_cert_url',
                'client_x509_cert_url', 'universe_domain'
            ]

            for key in expected_fields:
                if key not in data:
                    raise serializers.ValidationError(
                        detail={'google_sheets': f'Field "{key}" is missing from the credentials file'})

            instance, created = DatabaseProvider.objects.update_or_create(
                defaults={'google_sheet_credentials': data},
                database_schema_id=kwargs.get('pk')
            )

            return Response(self.get_response_serializer(instance), status=status.HTTP_201_CREATED)
        elif serializer.validated_data.get('airtable'):
            serializer.save()
            return Response({'status': True}, status=status.HTTP_200_OK)
        return Response({'connected': False}, status=status.HTTP_400_BAD_REQUEST)
