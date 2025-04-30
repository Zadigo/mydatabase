import pathlib

import pandas
import requests
from datasources import utils
from datasources.models import DataSource
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.base import File
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from rest_framework import fields
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import Serializer

from dataset_backend.choices import ColumnTypeChoices


class UserSerializer(Serializer):
    """Serializer for a user"""
    id = fields.IntegerField()


class DataSourceSerializer(Serializer):
    """Serializer for sheets"""

    id = fields.IntegerField(read_only=True)
    user = UserSerializer(read_only=True)
    name = fields.CharField()
    data_source_id = fields.CharField()
    google_sheet_url = fields.URLField()
    csv_based = fields.BooleanField(read_only=True)
    csv_file = fields.FileField(read_only=True)
    columns = fields.JSONField(read_only=True)
    column_names = fields.JSONField(read_only=True)
    created_on = fields.DateTimeField()


class WebhookSerializer(Serializer):
    id = fields.IntegerField(read_only=True)
    data = fields.JSONField()


# ##################
# Validation Forms #
# ##################


class APIForm(Serializer):
    name = fields.CharField()
    url = fields.URLField()
    column_name = fields.CharField(allow_null=True)
    columns = fields.ListField()


class UploadDataSourceForm(Serializer):
    """Form that allows the user to either
    upload a csv file or call an API endpoint
    to create a local CSV file"""

    name = fields.CharField(validators=[])
    csv_file = fields.FileField(required=False, allow_null=True)
    endpoint_url = fields.URLField(required=False, allow_null=True)
    endpoint_data_key = fields.CharField(required=False, allow_null=True)
    columns_to_keep = fields.ListField(required=False, allow_null=True)

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        request = self._context['request']

        data = {}
        user = get_object_or_404(get_user_model(), pk=1)

        endpoint_url = validated_data.get('endpoint_url')
        if endpoint_url is not None:
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
            instance = DataSource.objects.create(user=user, **validated_data)

            df = pandas.DataFrame(data)
            columns_to_keep = validated_data.get('columns_to_keep', [])
            if columns_to_keep:
                actual_columns = set(df.columns)
                received_columns = set(columns_to_keep)
                invalid_columns = received_columns.difference(actual_columns)
                if invalid_columns:
                    raise ValidationError({
                        'columns': 'The column names are not valid'
                    })
                df = df[columns_to_keep]

            column_types = utils.create_column_data_types(df.columns)
            instance.columns = column_types

            path = pathlib.Path(settings.MEDIA_ROOT)
            path = path.joinpath('sheets', instance.data_source_id)
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
            instance = DataSource.objects.create(user=user, **validated_data)
        return instance


# class ColumnDataTypesColumns(Serializer):


class ColumnDataTypesForm(Serializer):
    column = fields.CharField()
    renamed_to = fields.CharField(
        required=False
    )
    column_type = fields.ChoiceField(
        ColumnTypeChoices.choices,
        default='Text'
    )


class LoadedDataSerializer(Serializer):
    columns = fields.ListField()
    count = fields.IntegerField()
    results = fields.JSONField()
