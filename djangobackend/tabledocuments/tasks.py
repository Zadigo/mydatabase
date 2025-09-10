import asyncio
import json
import pathlib
from typing import Any

import pandas
import requests
from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.files.base import ContentFile
from tabledocuments.logic.edit import load_document_by_url
from tabledocuments.logic.utils import (create_column_options,
                                        create_column_type_options)
from tabledocuments.models import TableDocument

logger = get_task_logger(__name__)


@shared_task
def update_document_relationship(lh_document_id: str, rh_document_id: str, relationship_fields: list[str] = [], select: list[str] = []):
    # Your document relationship update logic here
    pass


@shared_task
def get_google_sheet_data(sheet_id: str, range_name: str):
    # Your Google Sheets API fetching logic here
    pass


@shared_task
def get_airtable_data(base_id: str, table_name: str, view_name: str):
    # Your Airtable API fetching logic here
    pass


@shared_task
def update_document_options(document_uuid: str, path: str):
    """A trigger that gets fired once the document is created. It fixes
    traditional elements such as the columns the document encoding references
    the column names etc"""
    path = pathlib.Path(path)

    if path.exists() and path.is_file():
        df = pandas.read_csv(path)

        column_type_options = create_column_type_options(df.columns.tolist())
        column_options = create_column_options(df.columns.tolist())

        try:
            document = TableDocument.objects.get(document_uuid=document_uuid)
        except TableDocument.DoesNotExist:
            logger.error(f"Document with UUID {document_uuid} does not exist.")
        else:
            document.column_types = column_type_options
            document.column_options = column_options
            document.column_names = df.columns.tolist()
            document.save()
            logger.warning(
                f"Successfully updated document options: {document.name}")


@shared_task
def get_document_from_url(url: str, headers: dict[str, str] = {}):
    """Function used to load the content of document returned via an API endpoint
    as a json format. The content will be loaded and transformed back to a csv
    database file"""
    async def proxy_get_url():
        response, errors = await load_document_by_url(url, headers=headers)

        if errors:
            logger.error(f"Errors occurred while loading document from {url}: {errors}")
            return {'error': errors}

        if response is not None:
            if 'application/json' in response.headers.get('Content-Type', ''):
                logger.warning(
                    f"Successfully retrieved JSON document from {url}")
                return response.json()

            if 'application/csv' in response.headers.get('Content-Type', ''):
                logger.warning(
                    f"Successfully retrieved CSV document from {url}")
                return response.text
        else:
            logger.warning(
                "Failed to retrieve document from "
                f"{url}, status code: {response.content}"
            )
    
    async def main():
        t1 = asyncio.create_task(proxy_get_url())
        return await t1

    return asyncio.run(main())


@shared_task
def create_csv_file_from_data(data: Any, document_id: str | int, entry_key: str | None):
    if data is None:
        logger.warning(f'No data provided? Received {data}')
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
                string_data = json.dumps(data)
                logger.error(
                    'Object is a dictionnary and no '
                    f'entry key was provided: {string_data[:100]}...'
                )
                return

            if 'error' in data:
                return data

            try:
                data = data[entry_key]
            except KeyError:
                string_data = json.dumps(data)
                logger.error(f'Entry key {entry_key} not found in data: {string_data[:100]}...')
                return

        if isinstance(data, list):
            df = pandas.DataFrame(data)
            # file = df.to_feather(index=True, index_label='record_id')
            # document.file.save(f'{document.name}.feather', file)

            csv_content = df.to_csv(index=True, index_label='record_id', encoding='utf-8', doublequote=True)
            content = ContentFile(csv_content)
            document.file.save(f'{document.name}.csv', content)

        document.save()
        logger.warning(f"Successfully created Feather document: {document.name}")
