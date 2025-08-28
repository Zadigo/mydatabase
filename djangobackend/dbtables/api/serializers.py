from collections import namedtuple
from dbtables.models import DatabaseTable
from dbschemas.models import DatabaseSchema
from django.utils.crypto import get_random_string
from rest_framework import fields, serializers
from tabledocuments.api.serializer import SimpleDocumentSerializer
from tabledocuments.models import TableDocument
from dbtables.tasks import request_document_by_url, create_csv_file_from_data


class DatabaseTableSerializer(serializers.ModelSerializer):
    documents = SimpleDocumentSerializer(many=True, read_only=True)
    database = fields.IntegerField(write_only=True, required=False)

    class Meta:
        model = DatabaseTable
        exclude = ['database_schema']

    def validate(self, validated_data):
        try:
            database_id = validated_data.pop('database')
            instance = DatabaseSchema.objects.get(id=database_id)
        except:
            raise serializers.ValidationError('Database not found')

        validated_data['database_schema'] = instance
        return validated_data


class UploadFileSerializer(serializers.Serializer):
    """Serializer used to validate file uploads."""

    name = serializers.CharField(allow_blank=True, max_length=255)
    file = serializers.FileField(allow_null=True)
    url = serializers.URLField(allow_blank=True)
    entry_key = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    # google_sheet_id = serializers.CharField(allow_blank=True)

    def validate(self, data):
        name = data.get('name')
        file = data.get('file')
        url = data.get('url')
        # google_sheet_id = data.get('google_sheet_id')

        fields_are_none = [
            file is None,
            url is None,
        ]

        fields_are_blank = [
            file is None,
            url == ''
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

        if name is None and file is not None:
            file_extension = file.name.split('.')[-1]
            random_name = f'{get_random_string(32)}.{file_extension}'
            data['name'] = random_name
        else:
            data['name'] = data.get('name', get_random_string(32))

        return data

    def create(self, validated_data):
        request = self._context['request']
        table_id = request.parser_context['kwargs']['pk']

        # NOTE: Remove this for now because we do not
        # have the logic yet to upload Google Sheets
        # as a CSV to our backend
        # validated_data.pop('google_sheet_id')


        entry_key = None
        if 'entry_key' in validated_data:
            entry_key = validated_data.pop('entry_key')

            if entry_key == '':
                entry_key = None

        # TODO: Even when the tasks fails, the document
        # is still created. We should handle that case
        # and delete the document if the task fails or
        # not create the document until the task succeeds
        table = DatabaseTable.objects.get(id=table_id)
        document = TableDocument.objects.create(**validated_data)
        table.documents.add(document)

        if document.url and document.file == None:
            request_document_by_url.apply_async(
                args=[document.url],
                countdown=10,
                link=[
                    create_csv_file_from_data.s(document.pk, entry_key)
                ]
            )

        return document


class CustomCharField(fields.CharField):
    def run_validation(self, data):
        return super().run_validation(data)
