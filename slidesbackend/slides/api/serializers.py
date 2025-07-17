
from rest_framework import fields
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import Serializer

from sheets.api.serializers import SheetSerializer
from sheets.models import Sheet
from slides.api import validators
from slides.choices import (AccessChoices, ColumnTypeChoices, ComponentTypes,
                            InputTypeChoices, OperatorChoices, SortingChoices,
                            UnionChoices)
from slides.models import Slide


class UserSerializer(Serializer):
    """Serializer for a user"""
    id = fields.IntegerField()


class UserFiltersConditionForm(Serializer):
    """Validates the data for filters that
    the user can use in a slide"""

    column = fields.CharField(required=True)
    operator = fields.ChoiceField(
        OperatorChoices.choices,
        default=OperatorChoices.EQUALS
    )
    input_type = fields.ChoiceField(
        InputTypeChoices.choices,
        default=InputTypeChoices.INPUT
    )
    union = fields.ChoiceField(
        UnionChoices.choices,
        default=UnionChoices.AND
    )


class DataFiltersConditionForm(Serializer):
    """Validates slide data filters"""
    column = fields.CharField(required=True)
    operator = fields.ChoiceField(
        OperatorChoices.choices,
        default=OperatorChoices.EQUALS
    )
    value = fields.CharField()
    union = fields.ChoiceField(
        UnionChoices.choices,
        default=UnionChoices.AND
    )


class PermissionsConditionForm(Serializer):
    pass


class ConditionsForm(Serializer):
    """Validates slide conditions"""
    filters = DataFiltersConditionForm(many=True)


class BlockForm(Serializer):
    """Form that validates the creation of
    a new block for the given slide"""

    name = fields.CharField(required=False, allow_null=True)
    component = fields.ChoiceField(
        ComponentTypes.choices,
        default=ComponentTypes.TABLE_BLOCK,
    )
    record_creation_columns = fields.ListField()
    record_update_columns = fields.ListField()
    search_columns = fields.ListField()
    columns_visibility = fields.ListField()
    block_data_source = fields.URLField(
        required=False, 
        allow_null=True
    )
    conditions = ConditionsForm()
    user_filters = UserFiltersConditionForm(many=True)
    active = fields.BooleanField(default=True)


class UpdateBlockColumnForm(Serializer):
    """Serializer to update the single configuration
    for a column in a table block"""

    name = fields.CharField()
    column_type = fields.ChoiceField(
        ColumnTypeChoices.choices,
        default=ColumnTypeChoices.TEXT
    )
    column_sort = fields.ChoiceField(
        SortingChoices.choices,
        default=SortingChoices.NO_SORT
    )
    columns_visibility = fields.BooleanField(default=True)
    allow_record_creation = fields.BooleanField(default=True)
    allow_record_update = fields.BooleanField(default=True)

    def update(self, instance, validated_data):
        def filterout_current_column(columns):
            return list(filter(lambda x: x != validated_data['name'], columns))

        # Add or remove the field to the record creation field
        record_creation_columns = instance.record_creation_columns
        if validated_data['allow_record_creation']:
            record_creation_columns.append(validated_data['name'])
            instance.record_creation_columns = list(
                set(record_creation_columns))
        else:
            if validated_data['name'] in record_creation_columns:
                instance.record_creation_columns = filterout_current_column(
                    record_creation_columns
                )

        # Add or remove the field to the record update field
        record_update_columns = instance.record_creation_columns
        if validated_data['allow_record_update']:
            record_update_columns.append(validated_data['name'])
            instance.record_update_columns = list(set(record_update_columns))
        else:
            if validated_data['name'] in record_update_columns:
                instance.record_update_columns = filterout_current_column(
                    record_creation_columns
                )

        instance.save()
        return instance


class BlockSerializer(Serializer):
    """Represents a block on a page"""

    id = fields.IntegerField(read_only=True)
    name = fields.CharField()
    block_id = fields.CharField(read_only=True)
    component = fields.CharField()
    record_creation_columns = fields.ListField()
    record_update_columns = fields.ListField()
    visible_columns = fields.ListField()
    block_data_source = fields.URLField()
    data_source = fields.URLField()
    conditions = fields.JSONField()
    allow_record_creation = fields.BooleanField()
    allow_record_update = fields.BooleanField()
    allow_record_search = fields.BooleanField()
    user_filters = fields.JSONField()
    search_columns = fields.ListField()
    active = fields.BooleanField()
    modified_on = fields.DateTimeField()
    created_on = fields.DateTimeField()


###################
#      Slides     #
###################


class UpdateSlideForm(Serializer):
    """Serializer for updating a slide"""

    name = fields.CharField(
        required=True,
        allow_null=True
    )
    slide_data_source = fields.CharField(
        required=True,
        allow_null=True,
        validators=[validators.slide_data_source_validator]
    )

    def update(self, instance, validated_data):
        instance.name = validated_data['name']

        sheet_id = validated_data['slide_data_source']
        queryset = Sheet.objects.filter(sheet_id=sheet_id)
        if not queryset.exists():
            raise ValidationError({
                'sheet_data_source': 'Data source doest not exist'
            })
        instance.slide_data_source = sheet_id
        instance.save()
        return instance


class NewSlideForm(Serializer):
    name = fields.CharField(validators=[])
    access = fields.ChoiceField(
        AccessChoices.choices,
        default=AccessChoices.PUBLIC
    )

    def save(self, user, **kwargs):
        validated_data = {**self.validated_data, **kwargs}
        if self.instance is not None:
            self.instance = self.update(self.instance, validated_data)
        else:
            self.instance = self.create(user, validated_data)
        return self.instance

    def create(self, user, validated_data):
        instance = Slide.objects.create(user=user, **validated_data)
        return instance


class SlideSerializer(Serializer):
    """Represents a slide"""

    id = fields.IntegerField(read_only=True)
    user = UserSerializer(read_only=True)
    slide_id = fields.CharField(read_only=True)
    name = fields.CharField()
    sheets = SheetSerializer(many=True)
    blocks = BlockSerializer(many=True)
    slide_data_source = fields.URLField()
    access = fields.CharField()
    modified_on = fields.DateTimeField()
    created_on = fields.DateTimeField()
