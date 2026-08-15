import re

from rest_framework import fields, serializers
from rest_framework.exceptions import ValidationError

from dbschemas.models import DatabaseSchema
from dbtables.models import DatabaseTable
from tabledocuments.api.serializer import SimpleDocumentSerializer
from tabledocuments.choices import ColumnTypes


class DatabaseTableSerializer(serializers.ModelSerializer):
    documents = SimpleDocumentSerializer(many=True, read_only=True)
    database = fields.IntegerField(write_only=True, required=False)

    class Meta:
        model = DatabaseTable
        exclude = ('database_schema',)

    def validate(self, validated_data):
        if 'database' in validated_data:
            try:
                database_id = validated_data.pop('database')
                instance = DatabaseSchema.objects.get(id=database_id)
            except DatabaseSchema.DoesNotExist:
                raise serializers.ValidationError(detail={
                    'database': 'Database with this id does not exist'
                })

            validated_data['database_schema'] = instance
        print('validated_data', validated_data)
        return validated_data


class _ValidateColumnTypes(serializers.Serializer):
    name = fields.CharField()
    newName = fields.CharField()
    columnType = fields.ChoiceField(
        choices=ColumnTypes.choices,
        default=ColumnTypes.STRING
    )
    unique = fields.BooleanField(default=False)
    visible = fields.BooleanField(default=True)
    nullable = fields.BooleanField(default=True)

    def validate_new_name(self, value):
        # Name should not contain special
        # characters other than "_" or "-"
        if not re.match(r'^[\w-]+$', value):
            raise serializers.ValidationError({
                'newName': 'Column name can only contain letters, numbers, underscores, and hyphens'
            })
        return value


class _ValidateDocuments(serializers.Serializer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    name = serializers.CharField()
    url = serializers.URLField(
        allow_blank=True,
        allow_null=True
    )
    file = serializers.FileField(
        allow_null=True
    )
    entry_key = serializers.CharField(
        allow_blank=True,
        allow_null=True
    )
    source_type = serializers.ChoiceField(
        (
            ('file', 'File'),
            ('url', 'Url')
        )
    )
    content_type = serializers.ChoiceField(
        (
            ('json', 'JSON'),
            ('csv', 'CSV'),
            ('google_sheet', 'Google sheet')
        )
    )
    primary_key_field = serializers.BooleanField(
        default=False
    )

    def validate(self, attrs: dict):
        url = attrs.get('url')
        file = attrs.get('file')

        if url is None and file is None:
            raise ValidationError('Both url and file cannot be None')
        return attrs



class UploadFileSerializer(serializers.Serializer):
    """Serializer used to validate file uploads. In the specific
    case of using an url, the user can indicate an entry key that
    will be used to get the actual data nested in the JSON response."""

    name = serializers.CharField(
        max_length=255
    )
    using_columns = _ValidateColumnTypes(
        many=True
    )
    documents = _ValidateDocuments(
        many=True
    )
    merge = serializers.BooleanField(
        default=False
    )

    def validate(self, data: dict):
        name: str = data.get('name')
        data['name'] = name.lower().title()
        return data

    # def create(self, validated_data):
    #     request: Request = self._context['request']
    #     table_id = request.parser_context['kwargs']['pk']

    #     entry_key = None
    #     if 'entry_key' in validated_data:
    #         entry_key = validated_data.pop('entry_key')

    #         if entry_key == '':
    #             entry_key = None

    #     user_column_type_options = validated_data.pop('using_columns')

    #     column_type_serializer = _ValidateColumnTypes(
    #         data=user_column_type_options,
    #         many=True
    #     )

    #     try:
    #         column_type_serializer.is_valid(raise_exception=True)
    #     except ValidationError as e:
    #         field_errors = {}
    #         for error in e.detail:
    #             for field, errors in error.items():
    #                 field_errors[field] = str(errors[-1])
    #         raise ValidationError({'using_columns': field_errors})

    #     # At least one column should be visible
    #     column_type_json = column_type_serializer.validated_data
    #     column_state = list(map(lambda x: x['visible'], column_type_json))

    #     if not any(column_state):
    #         raise ValidationError('At least one column should be visible')

    #     # TODO: Even when the tasks fails, the document
    #     # is still created. We should handle that case
    #     # and delete the document if the task fails or
    #     # not create the document until the task succeeds
    #     table = DatabaseTable.objects.get(id=table_id)
    #     document = TableDocument.objects.create(**validated_data)
    #     table.documents.add(document)

    #     # When we are dealing with a file
    #     file = request.FILES.get('file', None)
    #     if file is not None:
    #         file_content = ''

    #         for chunk in file.chunks():
    #             file_content += chunk.decode('utf-8')

    #         if is_csv_file(file.name):
    #             tasks.create_csv_file_from_data.apply_async(
    #                 args=[
    #                     file_content,
    #                     document.pk,
    #                     column_type_json
    #                 ],
    #                 countdown=5
    #             )

    #         if is_json_file(file.name):
    #             tasks.create_json_file_from_data.apply_async(
    #                 args=[
    #                     file_content,
    #                     document.pk,
    #                     entry_key,
    #                     column_type_json
    #                 ],
    #                 countdown=5
    #             )

    #     # If we are dealing with an url, then we need to
    #     # create the csv document asynchronously
    #     if document.url and document.file is None:
    #         tasks.get_document_from_url.apply_async(
    #             args=[document.url],
    #             link=[
    #                 tasks.create_csv_file_from_data.s(
    #                     document.pk,
    #                     entry_key,
    #                     columns_serializer.validated_data
    #                 )
    #             ]
    #         )

    #     # In the same manner, if we have a google sheet id
    #     # we need to fetch the data from the sheet and create
    #     # the csv file locally
    #     if document.google_sheet_id and document.file is None:
    #         tasks.get_document_from_google_sheet.apply_async(
    #             args=[
    #                 table.id,
    #                 document.google_sheet_id
    #             ],
    #             link=[
    #                 tasks.create_csv_file_from_data.s(
    #                     document.pk, 
    #                     entry_key, 
    #                     columns_serializer.validated_data
    #                 )
    #             ]
    #         )
                
    #     return document
