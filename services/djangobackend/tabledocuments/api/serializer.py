from typing import Any

from rest_framework import fields, serializers

from tabledocuments.models import TableDocument
from tabledocuments.utils.validators import convert_to_types_models
from tabledocuments.validation_models import ColumnOptionsModel


class SimpleDocumentSerializer(serializers.ModelSerializer):
    """A serializer that returns the document details *without*
    the data it contains. It returns only metadata about the document."""

    column_names = fields.ListField(
        child=fields.CharField(),
        required=False
    )
    column_options = fields.ListField(
        child=fields.DictField(),
        required=False
    )
    column_types = fields.DictField(
        child=fields.ChoiceField(choices=["String", "Integer", "Float", "Boolean"]),
        required=False
    )

    class Meta:
        model = TableDocument
        fields = (
            'id', 
            'document_uuid', 
            'name', 
            'column_names',
            'column_options', 
            'column_types', 
            'updated_at', 
            'created_at'
        )

    def update(self, instance: TableDocument, validated_data: dict[str, Any]):
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
            failed_validation = []
            valid_items: list[ColumnOptionsModel] = []
            for option in validated_data['column_options']:
                model = ColumnOptionsModel(**option)
                if model.name not in instance.column_names:
                    failed_validation.append(option)
                    continue
                valid_items.append(model)

            if failed_validation:
                raise serializers.ValidationError({
                    'column_options': f'Failed validation for the following items: {failed_validation}'
                })

            for model in valid_items:
                for option in instance.column_options:
                    if option['name'] == model.name:
                        option.update(model.model_dump(exclude={'name', 'newName'}))

        # Only update column types if their actual value has changed
        if 'column_types' in validated_data:
            for model in convert_to_types_models(validated_data['column_types']):
                key = model.name
                value = model.columnType
                if instance.column_types[key] == value:
                    continue
                instance.column_types[key] = value

        instance.save()
        return instance
