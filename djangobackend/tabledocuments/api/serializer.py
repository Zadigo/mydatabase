from rest_framework import fields, serializers
from tabledocuments.choices import ColumnTypes
from tabledocuments.models import TableDocument


class SimpleDocumentSerializer(serializers.ModelSerializer):
    """A serializer that returns the document details *without*
    the data it contains. It returns only metadata about the document."""

    class Meta:
        model = TableDocument
        fields = [
            'id', 'document_uuid', 'name', 'column_names', 
            'column_types', 'column_options', 'updated_at', 'created_at'
        ]

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class _ColumnOptionsValidator(serializers.Serializer):
    name = fields.CharField()
    visible = fields.BooleanField(default=True)
    editable = fields.BooleanField(default=True)
    sortable = fields.BooleanField(default=True)
    searchable = fields.BooleanField(default=True)


class _ColumnTypesValidator(serializers.Serializer):
    name = fields.CharField()
    columnType = fields.ChoiceField(choices=ColumnTypes.choices, default=ColumnTypes.STRING)
    unique = fields.BooleanField(default=False)
    nullable = fields.BooleanField(default=True)


class UpdateColumnTypesSerializer(serializers.Serializer):
    """Serializer for updating column types of a TableDocument"""

    column_options = _ColumnOptionsValidator(many=True, required=False)
    column_types = _ColumnTypesValidator(many=True, required=False)

    def update(self, instance, validated_data):
        instance.column_types = validated_data.get('column_types', instance.column_types)
        instance.column_options = validated_data.get('column_options', instance.column_options)
        instance.save()
        return instance
