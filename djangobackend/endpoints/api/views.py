import datetime
import json
import pathlib

import pandas
from dbschemas.models import DatabaseSchema
from dbtables.models import DatabaseTable
from django.shortcuts import get_object_or_404
from django.utils import timezone
from endpoints import tasks
from endpoints.api.serializers import PublicApiEndpointSerializer
from endpoints.models import PublicApiEndpoint, SecretApiEndpoint
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView
from rest_framework.response import Response
from tabledocuments.models import TableDocument
from tabledocuments.tasks import update_document_options


class ApiEndpointRouterMixin:
    def get_object(self):
        endpoint = self.kwargs.get('endpoint')
        return get_object_or_404(self.queryset, endpoint=endpoint)


class SecretApiEndpointRouter(GenericAPIView, ApiEndpointRouterMixin):
    """This is the main router used for routing the external
    requests to the registered secret API endpoints. The user
    calls the endpoint with the method he wants to use just
    he would for a real one and then we route the request
    to the relevant endpoint."""

    queryset = SecretApiEndpoint.objects.all()

    def get(self, request, *args, **kwargs):
        endpoint = self.get_object()

    def post(self, request, *args, **kwargs):
        endpoint = self.get_object()

    def put(self, request, *args, **kwargs):
        endpoint = self.get_object()

    def patch(self, request, *args, **kwargs):
        endpoint = self.get_object()

    def delete(self, request, *args, **kwargs):
        endpoint = self.get_object()


class PublicApiEndpointRouter(GenericAPIView, ApiEndpointRouterMixin):
    """This is the main router used for routing the external
    requests to the registered public API endpoints. The user
    calls the endpoint with the method he wants to use just
    he would for a real one and then we route the request
    to the relevant endpoint."""

    queryset = PublicApiEndpoint.objects.all()
    lookup_field = 'endpoint'
    lookup_url_kwarg = 'endpoint'

    def forbidden_response(self):
        return Response(status=status.HTTP_403_FORBIDDEN)

    def fail_response(self, *messages):
        return Response({'error': list(messages)}, status=status.HTTP_400_BAD_REQUEST)

    def get_database(self):
        database = self.kwargs.get('database')
        return get_object_or_404(DatabaseSchema, id=database)

    def check_bearer_token(self, request):
        token = request.META.get('HTTP_X_TABLE_TOKEN')
        if not token:
            return False

        endpoint = self.get_object()

        if endpoint.bearer_token != token:
            return False
        return True

    def pre_request_check(self, request) -> bool | tuple[PublicApiEndpoint, DatabaseTable | None]:
        if not self.check_bearer_token(request):
            return False

        endpoint = self.get_object()

        requires_table = self.kwargs.get('table') is not None
        if requires_table:
            table = get_object_or_404(
                endpoint.database_schema.databasetable_set.all(),
                id=self.kwargs.get('table')
            )
            return endpoint, table
        return endpoint, None

    def create_table_request(self, request, table: DatabaseTable | None):
        """Creates a specific internal request for this endpoint
        and triggers a hit """
        template = {
            'resource': None,
            'database': None,
            'timestamp': timezone.now(),
            'count': 0,
            'results': []
        }

        def table_view(*args, **kwargs):
            if table is None:
                return Response(template, status=status.HTTP_200_OK)

            if not table.active_document_datasource:
                return Response(template, status=status.HTTP_200_OK)

            try:
                document = table.documents.get(
                    document_uuid=table.active_document_datasource)
            except Exception:
                return Response(template, status=status.HTTP_400_BAD_REQUEST)

            df = pandas.read_csv(pathlib.Path(document.file.path))

            tasks.create_hit.apply_async(
                args=[
                    self.get_object().endpoint,
                    table.database_schema.name,
                    table.name if table else None
                ],
                countdown=30
            )
            template['count'] = df.count()
            template['resource'] = self.request.path
            template['database'] = table.database_schema.id
            template['results'] = json.loads(df.to_json(orient='records'))
            return Response(template, status=status.HTTP_200_OK)

        return table_view(request=request)

    def get(self, request, *args, **kwargs):
        """This endpoint handles cases where the user
        wants to get data from a given resource."""
        state = self.pre_request_check(request)
        if not state:
            return self.forbidden_response()

        endpoint, table = state
        return self.create_table_request(request, table)

    def post(self, request, *args, **kwargs):
        state = self.pre_request_check(request)
        if not state:
            return self.forbidden_response()

        endpoint, table = state

        try:
            document: TableDocument = table.documents.get(
                document_uuid=table.active_document_datasource)
        except Exception:
            return self.fail_response()

        data = request.data
        if isinstance(data, dict):
            newdf = pandas.DataFrame([data])

            errored_columns = []
            for column in newdf.columns:
                if column not in document.column_names:
                    errored_columns.append(column)

            if errored_columns:
                return self.fail_response(
                    f"Columns {', '.join(errored_columns)} do not exist in the table schema.",
                    document.column_names
                )

            update_document_options.apply_async(
                args=[
                    str(document.document_uuid),
                    newdf.to_csv(index=False, encoding='utf-8',
                                 doublequote=True)
                ],
                countdown=40
            )

        print(request.data)

        return self.create_table_request(request, table)

    def put(self, request, *args, **kwargs):
        state = self.pre_request_check(request)
        if not state:
            return self.forbidden_response()

    def patch(self, request, *args, **kwargs):
        state = self.pre_request_check(request)
        if not state:
            return self.forbidden_response()

    def delete(self, request, *args, **kwargs):
        state = self.pre_request_check(request)
        if not state:
            return self.forbidden_response()


class ListEndpoints(ListAPIView):
    queryset = PublicApiEndpoint.objects.all()
    serializer_class = PublicApiEndpointSerializer
    permission_classes = []


class CreateEndpoint(GenericAPIView):
    queryset = PublicApiEndpoint.objects.all()
    serializer_class = PublicApiEndpointSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        endpoint_path = request.data.get('endpoint', None)
        if endpoint_path is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        database = get_object_or_404(DatabaseSchema, id=kwargs.get('database'))
        instance = PublicApiEndpoint.objects.create(
            endpoint=endpoint_path, database_schema=database)

        qs = self.get_queryset()
        serializer = self.get_serializer(instance=qs, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
