import datetime
import json
import pathlib

import pandas
from dbschemas.models import DatabaseSchema
from dbtables.models import DatabaseTable
from django.shortcuts import get_object_or_404
from endpoints import tasks
from endpoints.models import PublicApiEndpoint, SecretApiEndpoint
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response


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

    def get_database(self):
        database = self.kwargs.get('database')
        return get_object_or_404(DatabaseSchema, name=database)

    def check_bearer_token(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            return False

        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            return False
        return token == f"Bearer {self.get_object().bearer_token}"

    def pre_request_check(self, request) -> bool | tuple[SecretApiEndpoint, DatabaseSchema, DatabaseTable | None]:
        if not self.check_bearer_token(request):
            return False

        endpoint = self.get_object()
        database = self.get_database()

        requires_table = self.kwargs.get('table') is not None
        if requires_table:
            table = get_object_or_404(database.dbtable_set.all(), name=self.kwargs.get('table'))

        return endpoint, database, table if requires_table else None

    def fail_response(self):
        return Response(status=403)

    def create_table_request(self, request, table: DatabaseTable):
        """Creates a specific internal request for this endpoint
        and triggers a hit """
        template = {
            'resource': None,
            'database': None,
            'timestamp': datetime.ddatetime.now(),
            'results': []
        }

        def view_wrapper(request):
            @api_view(http_method_names=['get'])
            def table_view(*args, **kwargs):
                # Implement the logic to create a table request
                if not table.active_document_datasource:
                    return template

                document = table.documents.get(docment_uuid=table.active_document_datasource)
                df = pandas.DataFrame(pathlib.Path(document.file.path))

                
                tasks.create_hit.apply_async(
                    args=[
                        self.get_object().endpoint,
                        table.database_schema.name,
                        table.name if table else None
                    ]
                )
                
                return Response(template, status=status.HTTP_200_OK)
            return table_view(request=request)
        
        return view_wrapper(request)

    def get(self, request, *args, **kwargs):
        """This endpoint handles cases where the user
        wants to get data from a given resource."""
        state = self.pre_request_check(request)
        if not state:
            return self.fail_response()

        endpoint, database, table = state

        if table is None:
            return self.create_table_request(request, table)

    def put(self, request, *args, **kwargs):
        state = self.pre_request_check(request)
        if not state:
            return self.fail_response()

    def patch(self, request, *args, **kwargs):
        state = self.pre_request_check(request)
        if not state:
            return self.fail_response()

    def delete(self, request, *args, **kwargs):
        state = self.pre_request_check(request)
        if not state:
            return self.fail_response()
