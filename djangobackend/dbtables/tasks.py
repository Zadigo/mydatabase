from typing import Any

import pandas
import requests
import pathlib
from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.files.base import ContentFile
from rest_framework import serializers
from tabledocuments.models import TableDocument
from tabledocuments.logic.utils import create_column_type_options, create_column_options

logger = get_task_logger(__name__)


@shared_task
def request_document_by_url(url: str, headers: dict[str, str] = {}):
    try:
        response = requests.get(url, headers=headers)
    except:
        message = f"Error occurred while requesting document from {url}"
        logger.error(message)
        return {'error': message}
    else:
        if response.status_code == 200:
            try:
                if 'application/json' in response.headers.get('Content-Type', ''):
                    logger.success(f"Successfully retrieved JSON document from {url}")
                    return response.json()
            except:
                message = f"Error occurred while processing JSON response from {url}"
                logger.error(message)
                return {'error': message}

            if 'application/csv' in response.headers.get('Content-Type', ''):
                logger.success(f"Successfully retrieved CSV document from {url}")   
                return response.text
    return None


@shared_task
def create_csv_file_from_data(data: Any, document_id: str | int, entry_key: str | None):
    if data is None:
        logger.warning('No data provided')
        return

    try:
        document = TableDocument.objects.get(id=document_id)
    except TableDocument.DoesNotExist:
        logger.error(f"Document with ID {document_id} does not exist.")
    else:
        if isinstance(data, str):
            content = ContentFile(data)
            document.file.save(f'{document.name}.csv', content)

        if isinstance(data, dict):
            if entry_key is None:
                logger.error('Object is a dictionnary and no entry key was provided')
                return
            data = data[entry_key]

        if isinstance(data, list):
            df = pandas.DataFrame(data)
            csv_content = df.to_csv(index=False)
            content = ContentFile(csv_content)
            document.file.save(f'{document.name}.csv', content)

        document.save()
        logger.success(f"Successfully created CSV document: {document.name}")


@shared_task
def post_document_creation_trigger(path: str):
    """A trigger that gets fired once the document is created. It fixes
    traditional elements such as the columns the document encoding references
    the column names etc"""
    path = pathlib.Path(path)

    if path.exists() and path.is_file():
        df = pandas.read_csv(path)

        column_type_options = create_column_type_options(df.columns.tolist())
        column_options = create_column_options(df.columns.tolist())
