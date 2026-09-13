from rest_framework import fields, serializers

from tabledocuments.logic.utils import create_column_options_from_dict, resolve_models
from tabledocuments.models import TableDocument


class SimpleDocumentSerializer(serializers.ModelSerializer):
    """A serializer that returns the document details *without*
    the data it contains. It returns only metadata about the document."""

    class Meta:
        model = TableDocument
        fields = (
            'id', 'document_uuid', 'name', 'column_names',
            'column_options', 'column_types', 'updated_at', 'created_at'
        )

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class UpdateDocumentSerializer(serializers.ModelSerializer):
    """A serializer that returns the document details *without*
    the data it contains. It returns only metadata about the document."""

    column_options = fields.ListField(
        child=fields.DictField(), 
        required=False
    )

    class Meta:
        model = TableDocument
        fields = (
            'name',
            'document_uuid',
            'column_names', 
            'column_options'
        )

    def validate_name(self, value):
        return value

    def update(self, instance: TableDocument, validated_data: dict):
        instance.name = validated_data.get('name', instance.name)

        if 'column_options' in validated_data:
            values = create_column_options_from_dict(validated_data['column_options'])
            instance.column_options = resolve_models(values)

        instance.save()
        return instance
