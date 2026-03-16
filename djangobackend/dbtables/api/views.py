from dbtables.api.serializers import (DatabaseTableSerializer,
                                      UploadFileSerializer)
from dbtables.models import DatabaseTable
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from rest_framework.response import Response
from tabledocuments.api.serializer import SimpleDocumentSerializer
from rest_framework.request import Request
import pandas
from tabledocuments.logic.utils import create_column_type_options

class UpdateTable(RetrieveUpdateDestroyAPIView):
    """Endpoint used to update metadata for a 
    database table."""

    queryset = DatabaseTable.objects.all()
    serializer_class = DatabaseTableSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'
    permission_classes = []


class CheckoutDocument(GenericAPIView):
    """Endpoint used to checkout a document for a given table.
    The file is parsed and a sample of the data is returned to the client."""

    def post(self, request: Request, pk, *args, **kwargs):
        qs = DatabaseTable.objects.filter(pk=pk)
        table = qs.first()

        if table is None:
            return Response({'error': 'Table document not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        file = request.FILES.get('file')
        if file is None:
            return Response({'error': 'No file provided.'}, status=status.HTTP_400_BAD_REQUEST)

        df = None

        if file.name.endswith('.csv'):
            df = pandas.read_csv(file)

        if file.name.endswith('.json'):
            df = pandas.read_json(file)

        if df is None:
            return Response({'error': 'Unsupported file format. Please upload a CSV or JSON file.'}, status=status.HTTP_400_BAD_REQUEST)
            
        sample = df.head(2).to_dict(orient='records')

        template = {
            'sample': sample,
            'numberOfRows': df.shape[0],
            'numberOfColumns': df.shape[1],
            'columns': df.columns.tolist(),
            'columnTypes': create_column_type_options(df.columns.tolist()),
        }

        return Response(template, status=status.HTTP_200_OK)


class UploadNewDocument(CreateAPIView):
    """Endpoint used to upload a new file as a document
    or either via an url. The file is parsed and stored
    in the database."""

    queryset = DatabaseTable.objects.all()
    serializer_class = UploadFileSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        response_serializer = SimpleDocumentSerializer(
            instance=serializer.instance
        )
        
        template = {
            'id': response_serializer.data.get('id'), 
            'document_uuid': response_serializer.data.get('document_uuid')
        }
        return Response(template, status=status.HTTP_201_CREATED, headers=headers)


class CreateTable(CreateAPIView):
    """Endpoint used to create a new database table."""

    queryset = DatabaseTable.objects.all()
    serializer_class = DatabaseTableSerializer
    permission_classes = []
