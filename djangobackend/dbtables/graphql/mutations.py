from graphene_django.rest_framework.mutation import SerializerMutation
from dbtables.api.serializers import UploadFileSerializer

class CreateTableDocument(SerializerMutation):
    class Meta:
        serializer_class = UploadFileSerializer
        model_operations = ['create']
        lookup_field = 'document_uuid'
