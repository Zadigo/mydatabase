import json
from operator import itemgetter
from typing import Generic, Optional, TypeVar

import pandas
from datasources import models, utils
from datasources.api import serializers
from django.core.cache import cache
from django.db import transaction
from django.db.models import F, QuerySet
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotAcceptable, ValidationError
from rest_framework.response import Response

D = TypeVar('D', bound='models.DataSource')


class ListDataSources(Generic[D], generics.ListAPIView):
    """Returns all the sheets that a user has linked
    to his pages"""
    queryset = models.DataSource.objects.all()
    serializer_class = serializers.DataSourceSerializer

    def get_queryset(self) -> QuerySet[D]:
        qs = super().get_queryset()
        return qs.filter(user__id=1)


class UploadDataSource(Generic[D], generics.CreateAPIView):
    queryset = models.DataSource.objects.all()
    serializer_class = serializers.UploadDataSourceForm
    cache: D | None = None

    def perform_create(self, serializer):
        self.cache = serializer.save()

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        if self.cache is not None:
            serializer = serializers.DataSourceSerializer(instance=self.cache)
            self.cache = None
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)


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
    serializer = serializers.DataSourceSerializer(
        instance=data_sources, many=True)
    return Response(serializer.data)


class LoadDataSource(Generic[D], generics.GenericAPIView):
    queryset = models.DataSource.objects.all()
    serializer_class = serializers.LoadedDataSerializer

    def get_queryset(self) -> QuerySet[D]:
        qs = super().get_queryset()
        return qs.filter(user__id=1)

    def get(self, request, *args, **kwargs):
        data_source_id = self.kwargs['data_source_id']

        qs = self.get_queryset()
        instance = get_object_or_404(qs, data_source_id=data_source_id)

        serializer = serializers.DataSourceSerializer(instance=instance)
        return_data = serializer.data

        df: pandas.DataFrame = cache.get(f'{data_source_id}_data', None)
        if df is None:
            df = pandas.read_csv(instance.csv_file.path)

        sortby = request.GET.get('sortby')

        if sortby is not None:
            if sortby not in df.columns:
                raise ValidationError({'sortby': 'Column does not exist'})
            df = df.sort_values(sortby)

        return_data['columns'] = df.columns
        return_data['count'] = df[df.columns[0]].count()

        str_data = df.to_json(orient='records', force_ascii=False)
        return_data['results'] = json.loads(str_data)

        serializer = self.get_serializer(data=return_data)
        serializer.is_valid(raise_exception=True)
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


class UpdateColumnDataTypes(Generic[D], generics.GenericAPIView):
    """Update the column data types for the specified
    data source"""
    queryset = models.DataSource.objects.all()
    serializer_class = serializers.ColumnDataTypesForm

    def get_queryset(self) -> QuerySet[D]:
        qs = super().get_queryset()
        return qs.filter(user__id=1)

    def post(self, request, **kwargs):
        data_source_id = self.kwargs['data_source_id']

        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            qs = self.get_queryset()

            data_source = get_object_or_404(
                qs,
                data_source_id=data_source_id,
                user__id=1
            )

            df = pandas.read_csv(data_source.csv_file.path)

            # TODO: Utils
            invalid_columns = []
            for item in serializer.validated_data:
                exists = item['column'] in df.columns
                if not exists:
                    invalid_columns.append(item['column'])
                    continue

            if invalid_columns:
                raise ValidationError('Columns are not valid')

            data_source.column_types = serializer.validated_data
            data_source.save()
            sid1 = transaction.savepoint()

            renaming_mapper = {}
            for item in serializer.validated_data:
                rename_to = item.get('renamed_to', None)

                if rename_to is None:
                    continue

                renaming_mapper[item['column']] = item['renamed_to']

            if renaming_mapper:
                df = df.rename(columns=renaming_mapper)
                df.to_csv(data_source.csv_file.path)

            transaction.savepoint_commit(sid1)
        return Response(serializer.data)
