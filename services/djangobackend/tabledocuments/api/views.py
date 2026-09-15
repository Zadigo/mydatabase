from pydantic import ValidationError as PydanticValidationError
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from tabledocuments.api.serializer import (
    SimpleDocumentSerializer,
    UpdateDocumentSerializer,
)
from tabledocuments.models import TableDocument
from tabledocuments.validation_models import (
    OptionalColumnOptionsModel,
)


class RetrieveUpdateDestroyDocument(RetrieveUpdateDestroyAPIView):
    """Returns simple information about the given
    document (without the data it contains) or deletes
    or updates part of it"""

    queryset = TableDocument.objects.all()
    serializer_class = SimpleDocumentSerializer
    lookup_field = 'document_uuid'
    lookup_url_kwarg = 'document_uuid'
    permission_classes = ()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = UpdateDocumentSerializer(
            instance=instance, 
            data=request.data, 
            partial=partial
        )
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)
        response_serializer = self.get_serializer(instance)
        return Response(response_serializer.data)


# @extend_schema_serializer(
#     examples = [
#          OpenApiExample(
#             'Column options',
#             summary='short summary',
#             description='longer description',
#             value=[
#                 {
#                     'name': 'string'
#                 }
#             ],
#             # request_only=True, # signal that example only applies to requests
#             response_only=True, # signal that example only applies to responses
#         ),
#     ]
# )
class UpdateColumnTypes(GenericAPIView):
    """View to update the column types of a given document.
    Column types are a mapping of column names to their data types."""

    queryset = TableDocument.objects.all()
    http_method_names = ('patch',)
    permission_classes = ()

    def patch(self, request: Request, *args, **kwargs):
        instance: TableDocument = self.get_object()

        _copied_data = request.data.copy()
        if 'name' in _copied_data:
            _copied_data.pop('name')

        try:
            model = OptionalColumnOptionsModel(**_copied_data)
        except PydanticValidationError as e:
            raise ValidationError(f"Invalid column options: {e}")
        else:
            validated_data = model.model_dump(exclude_none=True)

            instance.column_options = validated_data.get('column_options', instance.column_options)
            instance.save()

            return Response(validated_data  )
