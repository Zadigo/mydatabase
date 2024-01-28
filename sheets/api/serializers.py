import pathlib

import pandas
import requests
from django.conf import settings
from django.core.files.base import File
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from rest_framework import fields
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import Serializer
from my_database.choices import ColumnTypeChoices

from sheets.models import USER_MODEL, Sheet


class UserSerializer(Serializer):
    """Serializer for a user"""
    id = fields.IntegerField()


class SheetSerializer(Serializer):
    """Serializer for sheets"""

    id = fields.IntegerField(read_only=True)
    user = UserSerializer(read_only=True)
    name = fields.CharField()
    sheet_id = fields.CharField()
    url = fields.URLField()
    csv_based = fields.BooleanField(read_only=True)
    csv_file = fields.FileField(read_only=True)
    columns = fields.JSONField(read_only=True)
    column_types = fields.JSONField(read_only=True)
    created_on = fields.DateTimeField()


class WebhookSerializer(Serializer):
    data = fields.JSONField()


# ##################
# Validation Forms #
# ##################


class APIForm(Serializer):
    name = fields.CharField()
    url = fields.URLField()
    column_name = fields.CharField(allow_null=True)
    columns = fields.ListField()


class UploadSheetForm(Serializer):
    """Form that allows the user to upload a
    csv file to his database"""

    name = fields.CharField(validators=[])
    csv_file = fields.FileField(required=False, allow_null=True)
    endpoint_url = fields.URLField(required=False, allow_null=True)
    endpoint_data_key = fields.CharField(required=False, allow_null=True)
    columns = fields.ListField(required=False, allow_null=True)

    def save(self, request, **kwargs):
        setattr(self, 'request', request)
        return super().save(**kwargs)

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        data = {}
        user = get_object_or_404(USER_MODEL, pk=1)

        endpoint_url = validated_data.get('endpoint_url')
        if endpoint_url:
            headers = {'content-type': 'application/json'}
            response = requests.get(endpoint_url, headers=headers)
            if response.status_code == 200:
                data = response.json()

                endpoint_data_key = validated_data.get('endpoint_data_key')
                if endpoint_data_key is not None:
                    try:
                        data = data[endpoint_data_key]
                    except Exception as e:
                        raise fields.ValidationError({
                            'endpoint_data_key': "Column does not exist in dataset"
                        })
            instance = Sheet.objects.create(user=user, **validated_data)

            df = pandas.DataFrame(data)
            columns = validated_data.get('columns', [])
            if columns:
                actual_columns = set(df.columns)
                received_columns = set(columns)
                invalid_columns = received_columns.difference(actual_columns)
                if invalid_columns:
                    raise ValidationError({
                        'columns': 'The column names are not valid'
                    })
                df = df[columns]

            # TODO: Use a unique function to normalize
            # the creation of the column_types
            column_types = [
                {'column': column, 'type': 'Text'}
                for column in list(df.columns)
            ]
            instance.columns = list(df.columns)
            instance.column_types = column_types

            path = pathlib.Path(settings.MEDIA_ROOT)
            path = path.joinpath('sheets', instance.sheet_id)
            if not path.exists():
                path.mkdir()

            temp_filename = get_random_string(length=5)
            path = path.joinpath(f'{temp_filename}_file.csv')
            df.to_csv(path, index=False, encoding='utf-8')

            with open(path, mode='r', encoding='utf-8') as f:
                file = File(f)
                instance.csv_file = file
                instance.save()
        else:
            instance = Sheet.objects.create(user=user, **validated_data)
        return instance


class ColumnDataTypesForm(Serializer):
    column = fields.CharField()
    # renamed_to = fields.CharField(required=False)
    type = fields.ChoiceField(
        ColumnTypeChoices.choices,
        default=ColumnTypeChoices.TEXT
    )
