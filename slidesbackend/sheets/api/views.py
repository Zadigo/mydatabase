import json

import pandas
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotAcceptable, ValidationError
from rest_framework.response import Response

from sheets import models
from sheets.api import serializers


@api_view(http_method_names=['post'])
def upload_csv_file(request, **kwargs):
    """Upload a new csv file to create a new connection"""
    serializer = serializers.UploadSheetForm(data=request.data)
    serializer.is_valid(raise_exception=True)
    instance = serializer.save(request=request)
    serialized_data = serializers.SheetSerializer(instance=instance)
    return Response(serialized_data.data)


@api_view(http_method_names=['get'])
def load_csv_file_data(request, sheet_id, **kwargs):
    """Load and return the content of previously uploaded
    CSV file. This is mainly done to reload data to
    the frontend without passing via the Google sheet"""
    instance = get_object_or_404(models.Sheet, sheet_id=sheet_id)

    serializer = serializers.SheetSerializer(instance=instance)
    return_data = serializer.data
    file = instance.csv_file.open(mode='r')
    df = pandas.read_csv(file)

    sort_by = request.GET.get('sort_by')
    # unique_values = request.GET.get('unique_values', 0)
    # unique_values = True if unique_values == 1 else False

    if sort_by is not None:
        if sort_by not in df.columns:
            raise ValidationError({'sort_by': 'Column does not exist'})
        df = df.sort_values(sort_by)

    return_data['columns'] = df.columns
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
def user_sheets(request, **kwargs):
    """Returns all the sheets that a user has linked
    to his pages"""
    user = get_object_or_404(models.USER_MODEL, pk=1)
    queryset = models.Sheet.objects.filter(user=user)
    serializer = serializers.SheetSerializer(instance=queryset, many=True)
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
