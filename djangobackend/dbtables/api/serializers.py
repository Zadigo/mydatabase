import re

from dbschemas.models import DatabaseSchema
from dbtables.models import DatabaseTable
from rest_framework import fields, serializers
from rest_framework.exceptions import ValidationError
from tabledocuments import tasks
from tabledocuments.api.serializer import SimpleDocumentSerializer
from tabledocuments.choices import ColumnTypes
from tabledocuments.models import TableDocument


class DatabaseTableSerializer(serializers.ModelSerializer):
    documents = SimpleDocumentSerializer(many=True, read_only=True)
    database = fields.IntegerField(write_only=True, required=False)

    class Meta:
        model = DatabaseTable
        exclude = ['database_schema']

    def validate(self, validated_data):
        if 'database' in validated_data:
            try:
                database_id = validated_data.pop('database')
                instance = DatabaseSchema.objects.get(id=database_id)
            except:
                raise serializers.ValidationError(detail={
                    'database': 'Database with this id does not exist'
                })

            validated_data['database_schema'] = instance
        return validated_data


class _ValidateColumnTypes(serializers.Serializer):
    name = fields.CharField()
    new_name = fields.CharField()
    column_type = fields.ChoiceField(
        choices=ColumnTypes.choices, default=ColumnTypes.STRING)
    unique = fields.BooleanField(default=False)
    visible = fields.BooleanField(default=True)
    nullable = fields.BooleanField(default=True)

    def validate_new_name(self, value):
        # Name should not contain special
        # characters other than "_" or "-"
        if not re.match(r'^[\w-]+$', value):
            raise serializers.ValidationError({
                'new_name': 'Column name can only contain letters, numbers, underscores, and hyphens'
            })
        return value


class UploadFileSerializer(serializers.Serializer):
    """Serializer used to validate file uploads. In the specific
    case of using an url, the user can indicate an entry key that
    will be used to get the actual data nested in the JSON response."""

    name = serializers.CharField(
        max_length=255
    )
    file = serializers.FileField(
        allow_null=True
    )
    url = serializers.URLField(
        allow_blank=True
    )
    entry_key = serializers.CharField(
        allow_null=True,
        allow_blank=True,
        required=False
    )
    google_sheet_id = serializers.CharField(
        allow_null=True,
        allow_blank=True
    )
    using_columns = serializers.JSONField(write_only=True)

    def validate(self, data):
        name = data.get('name')
        file = data.get('file')
        url = data.get('url')
        google_sheet_id = data.get('google_sheet_id')

        fields_are_none = [
            file is None,
            url is None,
            google_sheet_id is None
        ]

        fields_are_blank = [
            file is None,
            url == '',
            google_sheet_id == ''
        ]

        if any([all(fields_are_none), all(fields_are_blank)]):
            raise serializers.ValidationError(
                'Either a file, a URL, or a Google Sheet ID '
                'must be provided'
            )

        # Check the size of the file which can be
        # overwhelming if too big
        if file is not None and file.size > 50 * 1024 * 1024:
            raise serializers.ValidationError(
                'File size must be less than 50MB'
            )

        # if name is None and file is not None:
        #     file_extension = file.name.split('.')[-1]
        #     random_name = f'{get_random_string(32)}.{file_extension}'
        #     data['name'] = random_name
        # else:
        data['name'] = data.get('name')
        return data

    def create(self, validated_data):
        request = self._context['request']
        table_id = request.parser_context['kwargs']['pk']

        entry_key = None
        if 'entry_key' in validated_data:
            entry_key = validated_data.pop('entry_key')

            if entry_key == '':
                entry_key = None

        column_options = validated_data.pop('using_columns')

        columns_serializer = _ValidateColumnTypes(data=column_options, many=True)
        columns_serializer.is_valid(raise_exception=True)

        # At least one column should be visible
        column_state = map(lambda x: x['visible'], columns_serializer.validated_data)
        if not any(column_state):
            raise ValidationError('At least one column should be visible')

        # TODO: Even when the tasks fails, the document
        # is still created. We should handle that case
        # and delete the document if the task fails or
        # not create the document until the task succeeds
        table = DatabaseTable.objects.get(id=table_id)
        document = TableDocument.objects.create(**validated_data)
        table.documents.add(document)

        # When we are dealing with a file
        file = request.FILES.get('file', None)
        if file:
            tasks.create_csv_file_from_data.apply_async(
                args=[file.read(), document.pk, entry_key, columns_serializer.validated_data],
                countdown=5
            )

        # If we are dealing with an url, then we need to
        # create the csv document asynchronously
        if document.url and document.file == None:
            tasks.get_document_from_url.apply_async(
                args=[document.url],
                link=[tasks.create_csv_file_from_data.s(
                    document.pk, entry_key, columns_serializer.validated_data)]
            )

        # In the same manner, if we have a google sheet id
        # we need to fetch the data from the sheet and create
        # the csv file locally
        if document.google_sheet_id and document.file == None:
            providers = table.database_schema.databaseprovider_set.all()
            if providers.exists():
                try:
                    google_provider = providers.get(
                        has_google_sheet_connection=True)
                except:
                    raise ValidationError(
                        'No provider with Google Sheet connection found')
                tasks.get_document_from_google_sheet.apply_async(
                    args=[google_provider.google_service_account_credentials,
                          document.google_sheet_id],
                    link=[tasks.create_csv_file_from_data.s(
                        document.pk, entry_key, columns_serializer.validated_data)]
                )

        # Once the document is created, we need to populate
        # column_options, column_types and column_names
        tasks.update_document_options.apply_async(
            args=[
                str(document.document_uuid), 
                columns_serializer.validated_data
            ]
        )
        return document


class CustomCharField(fields.CharField):
    def run_validation(self, data):
        return super().run_validation(data)
