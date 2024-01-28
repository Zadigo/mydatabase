import json

import pandas
from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotAcceptable, ValidationError
from rest_framework.response import Response

from datasources import models, utils
from datasources.api import serializers


@api_view(http_method_names=['post'])
def upload_new_data_source(request, **kwargs):
    """Upload a new data source which can be a csv file,
    an API endpoint that will become a CSV file
    to create a new connection"""
    serializer = serializers.UploadDataSourceForm(data=request.data)
    serializer.is_valid(raise_exception=True)
    instance = serializer.save(request)
    serialized_data = serializers.DataSourceSerializer(instance=instance)
    return Response(serialized_data.data)


@api_view(http_method_names=['post'])
def delete_data_source(request, data_source_id, **kwargs):
    """Deletes an existing data source"""
    data_source = get_object_or_404(
        models.DataSource,
        user__id=1,
        data_source_id=data_source_id
    )
    data_source.delete()

    data_sources = models.DataSource.objects.filter(user__id=1)
    serializer = serializers.DataSourceSerializer(instance=data_sources, many=True)
    return Response(serializer.data)


@api_view(http_method_names=['get'])
def load_data_source_data(request, data_source_id, **kwargs):
    """Load and return the content of previously uploaded
    CSV file. This is mainly done to reload data to
    the frontend without passing via the Google sheet"""
    instance = get_object_or_404(
        models.DataSource,
        data_source_id=data_source_id
    )

    serializer = serializers.DataSourceSerializer(instance=instance)
    return_data = serializer.data

    file = instance.csv_file.open(mode='r')
    df = pandas.read_csv(file)

    sort_by = request.GET.get('sort_by')

    if sort_by is not None:
        if sort_by not in df.columns:
            raise ValidationError({'sort_by': 'Column does not exist'})
        df = df.sort_values(sort_by)

    # return_data['columns'] = df.columns
    return_data['count'] = df[df.columns[0]].count()
    return_data['results'] = json.loads(
        df.to_json(
            orient='records',
            force_ascii=False
        )
    )

    file.close()
    return Response(data=return_data)


@api_view(http_method_names=['get'])
def list_user_data_sources(request, **kwargs):
    """Returns all the sheets that a user has linked
    to his pages"""
    # TODO: Use request.user
    queryset = models.DataSource.objects.filter(user__id=1)
    serializer = serializers.DataSourceSerializer(instance=queryset, many=True)
    return Response(data=serializer.data)


@api_view(http_method_names=['post'])
def send_to_webhook(request, webhook_id, **kwargs):
    instance = get_object_or_404(models.Webhook, webhook_id=webhook_id)

    # If the person spams the webhook,
    # block any other incoming requests
    current_date = now()
    total_seconds = round(
        (current_date - instance.last_usage).total_seconds(), 1
    )
    if total_seconds < 3:
        raise NotAcceptable('Upload rate exceeded')

    instance.usage = F('usage') + 1
    instance.last_usage = current_date
    instance.save()

    serializer = serializers.WebhookSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    df = pandas.DataFrame(serializer.data['data'])
    columns = df.columns
    return_data = {
        'count': df[columns[0]].count(),
        'colums': columns
    }
    return Response(data=return_data)


@api_view(http_method_names=['post'])
def update_column_data_types(request, data_source_id, **kwargs):
    """Update the column data types for the specified
    data source"""
    serializer = serializers.ColumnDataTypesForm(data=request.data, many=True)
    serializer.is_valid(raise_exception=True)

    with transaction.atomic():
        data_source = get_object_or_404(
            models.DataSource,
            data_source_id=data_source_id,
            user__id=1
        )
        data_source.column_types = serializer.validated_data
        data_source.save()
        sid1 = transaction.savepoint()

        # df = pandas.DataFrame(data_source.csv_file.path)
        # renaming_mapper = {}
        # for item in serializer.validated_data:
        #     rename_to = item.get('renamed_to', None)
        #     if rename_to is None:
        #         continue
        #     renaming_mapper[item['column']] = item['renamed_to']

        # df = df.rename(columns=renaming_mapper)
        # df.to_csv(data_source.csv_file.path)

        transaction.savepoint_commit(sid1)
    return Response({'state': True})


