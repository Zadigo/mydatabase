
import pandas
from django.shortcuts import get_object_or_404
from rest_framework import fields
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.serializers import Serializer

from datasources import models as sheets_models
from datasources.api.serializers import DataSourceSerializer
from datasources.models import DataSource
from slides import models as slides_models
from slides.api import utils, validators
from slides.api.utils import list_manager
from slides.choices import (AccessChoices, ColumnTypeChoices, ComponentTypes,
                            InputTypeChoices, OperatorChoices, SortingChoices,
                            UnionChoices)
from slides.models import Slide
from django.contrib.auth import get_user_model


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
    """Validates block conditions"""
    filters = DataFiltersConditionForm(many=True)
    columns_visibility = fields.ListField()


class BlockForm(Serializer):
    """Form that validates the creation of
    a new block for the given slide. Block can
    be created in two different manners:
        * Simple creation: just component type
    """

    name = fields.CharField(required=False, allow_null=True)
    component = fields.ChoiceField(
        ComponentTypes.choices,
        default='Table block',
    )
    record_creation_columns = fields.ListField(required=False)
    record_update_columns = fields.ListField(required=False)
    search_columns = fields.ListField(required=False)
    block_data_source = fields.URLField(
        required=False,
        allow_null=True
    )
    conditions = ConditionsForm(required=False)
    user_filters = UserFiltersConditionForm(many=True, required=False)
    active = fields.BooleanField(default=True)

    def create(self, validated_data):
        request = self._context['request']
        slide_id = self._context['slide_id']

        user = get_object_or_404(get_user_model(), pk=1)
        slide = get_object_or_404(
            slides_models.Slide,
            user=user,
            slide_id=slide_id
        )

        block = slide.blocks.create(**validated_data)
        # Set these fields to be able to implement
        # specific actions (visibility, updating...)
        # on the columns for this block individually
        data_source = slide.slide_data_source
        if data_source is not None:
            true_false_dictionnaries = utils.flatten_dictionnaries(data_source.columns)
            block.record_creation_columns = true_false_dictionnaries
            block.record_update_columns = true_false_dictionnaries
            block.search_columns = true_false_dictionnaries
            block.visible_columns = true_false_dictionnaries
            block.save()

        return block

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


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
    column_visibility = fields.BooleanField(default=True)
    allow_record_creation = fields.BooleanField(default=True)
    allow_record_update = fields.BooleanField(default=True)
    allow_record_search = fields.BooleanField(default=True)

    def update(self, instance, validated_data):
        instance = list_manager(
            instance,
            'record_creation_columns',
            validated_data['name']
        )

        instance = list_manager(
            instance,
            'record_update_columns',
            validated_data['name']
        )

        instance = list_manager(
            instance,
            'visible_columns',
            validated_data['name']
        )

        # # Add or remove the field to the record creation field
        # record_creation_columns = instance.record_creation_columns
        # if validated_data['allow_record_creation']:
        #     record_creation_columns.append(validated_data['name'])
        # else:
        #     index_of_column = record_creation_columns.index(
        #         validated_data['name'])
        #     record_creation_columns.pop(index_of_column)

        # instance.record_creation_columns = record_creation_columns

        # # Add or remove the field to the record update field
        # record_update_columns = instance.record_update_columns
        # if validated_data['allow_record_creation']:
        #     record_update_columns.append(validated_data['name'])
        # else:
        #     index_of_column = record_update_columns.index(
        #         validated_data['name'])
        #     record_update_columns.pop(index_of_column)

        # # Add or remove the field to the record update field
        # visible_columns = instance.visible_columns
        # if validated_data['columns_visibility']:
        #     visible_columns.append(validated_data['name'])
        # else:
        #     index_of_column = visible_columns.index(
        #         validated_data['name'])
        #     visible_columns.pop(index_of_column)

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
    block_data_source = DataSourceSerializer()
    active_data_source = DataSourceSerializer()
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
    """Serializer for updating the data for 
    a given slide"""

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
        name = validated_data.get('name', None)
        if name is not None:
            instance.name = name

        data_source_id = validated_data.get('slide_data_source', None)

        if data_source_id is not None:
            queryset = DataSource.objects.filter(data_source_id=data_source_id)

            if not queryset.exists():
                raise NotFound({
                    'sheet_data_source': 'Data source doest not exist'
                })

            try:
                instance.slide_data_source = queryset.get()
            except:
                raise ValidationError({
                    'sheet_data_source': 'Could not get a valid data source'
                })

        instance.save()
        return instance


class NewSlideForm(Serializer):
    name = fields.CharField(validators=[])
    access = fields.ChoiceField(
        AccessChoices.choices,
        default=AccessChoices.PUBLIC
    )

    def create(self, validated_data):
        # request = self._context['request']
        # instance = Slide.objects.create(
        #     user=request.user,
        #     **validated_data
        # )
        # return instance

        # TESTING
        instance = Slide.objects.create(
            user=get_user_model().objects.first(),
            **validated_data
        )
        return instance


class SlideSerializer(Serializer):
    """Represents a slide"""

    id = fields.IntegerField(read_only=True)
    user = UserSerializer(read_only=True)
    slide_id = fields.CharField(read_only=True)
    name = fields.CharField()
    blocks = BlockSerializer(many=True)
    slide_data_source = DataSourceSerializer()
    access = fields.CharField()
    modified_on = fields.DateTimeField()
    created_on = fields.DateTimeField()


class SlideFilteringForm(Serializer):
    """Validates the requests for filtering
    the data from a given slide"""

    slide_id = fields.CharField()
    data_source_id = fields.CharField()
    data = fields.JSONField()
    conditions = DataFiltersConditionForm(many=True)

    def create(self, validated_data):
        slide = Slide.objects.get(slide_id=validated_data['slide_id'])
        return slide
