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

    name = serializers.CharField(max_length=255, required=False)
    file = serializers.FileField(required=False)
    url = serializers.URLField(required=False)
    google_sheet_id = serializers.CharField(required=False)

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

        if all(fields_are_none):
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
            file_extension = file.name.split(
                '.')[-1] if file is not None else None
            random_name = f'{get_random_string(32)}.{file_extension}'
            data['name'] = file.name if file is not None else random_name

        return data

    def create(self, validated_data):
        request = self._context['request']
        table_id = request.parser_context['kwargs']['pk']

        table = DatabaseTable.objects.get(id=table_id)
        document = TableDocument.objects.create(**validated_data)
        table.documents.add(document)

        print(document.url)

        request_document_by_url.apply_async(
            args=[document.url],
            countdown=10,
            link=create_csv_file_from_data.s(document.pk)
        )
        if document.url and document.file is None:
            print('apply_async')

        return document
