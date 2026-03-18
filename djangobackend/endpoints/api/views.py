
from rest_framework.exceptions import ValidationError
from asgiref.sync import async_to_sync
from dbschemas.models import DatabaseSchema
from django.shortcuts import get_object_or_404
from dbtables.models import DatabaseTable
from endpoints.validators import QueryValidator
from tabledocuments.logic.edit import DocumentEdition
from endpoints.api.serializers import PublicApiEndpointSerializer
from endpoints.models import ApiEndpoint, PublicApiEndpoint, SecretApiEndpoint
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from django.db.models import QuerySet
from django.core.cache import cache

class ApiEndpointRouterMixin[T = ApiEndpoint]:
    def get_queryset(self) -> QuerySet[T]:
        qs = cache.get('api_endpoints')
        if qs is not None:
            prefetched = self.queryset.prefetch_related('database_schema')
            qs = prefetched.all()
            cache.set('api_endpoints', qs, timeout=60*60) # Cache for 1 hour
        return qs

    def get_object(self) -> T:
        endpoint_uuid = self.kwargs.get(self.lookup_url_kwarg)
        return get_object_or_404(self.queryset, **{self.lookup_field: endpoint_uuid})
    
    def parse_bearer_token(self, request: Request) -> str | None:
        """Parses the bearer token from the Authorization header."""
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return None

        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return None

        return parts[1]


class SecretApiEndpointRouter(ApiEndpointRouterMixin[SecretApiEndpoint], GenericAPIView):
    """This is the main router used for routing the external
    requests to the registered secret API endpoints. The user
    calls the endpoint with the method he wants to use just
    he would for a real one and then we route the request
    to the relevant endpoint."""

    queryset = SecretApiEndpoint.objects.all()

    def get(self, request: Request, *args, **kwargs):
        endpoint = self.get_object()

    def post(self, request: Request, *args, **kwargs):
        endpoint = self.get_object()

    def put(self, request: Request, *args, **kwargs):
        endpoint = self.get_object()

    def patch(self, request: Request, *args, **kwargs):
        endpoint = self.get_object()

    def delete(self, request: Request, *args, **kwargs):
        endpoint = self.get_object()


class PublicApiEndpointRouter(ApiEndpointRouterMixin[PublicApiEndpoint], GenericAPIView):
    """This is the main router used for routing the external
    requests to the registered public API endpoints. The user
    calls the endpoint with the method he wants to use just
    he would for a real one and then we route the request
    to the relevant endpoint."""

    queryset = PublicApiEndpoint.objects.all()
    lookup_url_kwarg = 'endpoint_uuid'
    lookup_field = 'endpoint_uuid'

    def _pre_request_check(self, request: Request, method: str) -> PublicApiEndpoint:
        endpoint = self.get_object()
        token = self.parse_bearer_token(request)

        if endpoint.bearer_token is not None:
            if token is None or endpoint.bearer_token != token:
                raise ValidationError("Invalid or missing bearer token.")
            
        if method.upper() not in endpoint.methods:
            raise ValidationError(f"HTTP method {method} is not allowed for this endpoint.")
        
        return endpoint
    
    def _dispatch_request(self, request: Request, database: str, table: str):
        """This method is responsible for dispatching the request to the relevant
        database and table based on the endpoint configuration. It also handles
        the authentication and authorization of the request."""
        database = get_object_or_404(DatabaseSchema, id=database)
        tables: QuerySet[DatabaseTable] = database.databasetable_set.all()
        table: DatabaseTable = get_object_or_404(tables, id=table)
        
        try:
            instance = DocumentEdition()
            state, document = async_to_sync(instance.load_document_by_id)(table.active_document_datasource)
        except Exception as e:
            print(instance.errors)
            raise ValidationError(
                "An error occurred while loading the document datasource for the table.", 
                code="document_load_error"
            )

        if not state:
            raise ValidationError(
                "The table does not have an active document datasource.", 
                code="no_active_document"
            )
        
        return document

    def get(self, request: Request, *args, **kwargs):
        endpoint = self._pre_request_check(request, 'GET')
        document = self._dispatch_request(request, self.kwargs.get('database'), self.kwargs.get('table'))

        df = document.content.copy()

        query = request.query_params.dict()
        if query:
            validated_query = QueryValidator(**query)

            if validated_query.select is not None:
                df = df[validated_query.select.split(',')]

        data = df.to_json(orient='records')

        template = {
            'data': data,
            'resource': request.path,
            'database': self.kwargs.get('database'),
            'table': self.kwargs.get('table'),
        }

        return Response(template, status=status.HTTP_200_OK)
    
    def post(self, request: Request, *args, **kwargs):
        endpoint = self._pre_request_check(request, 'POST')
        return Response(status=status.HTTP_200_OK)
    
    def put(self, request: Request, *args, **kwargs):
        endpoint = self._pre_request_check(request, 'PUT')
        return Response(status=status.HTTP_200_OK)

    def patch(self, request: Request, *args, **kwargs):
        endpoint = self._pre_request_check(request, 'PATCH')
        return Response(status=status.HTTP_200_OK)

    def delete(self, request: Request, *args, **kwargs):
        endpoint = self._pre_request_check(request, 'DELETE')
        return Response(status=status.HTTP_200_OK)
    

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
