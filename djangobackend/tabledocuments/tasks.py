import asyncio
import csv
import io
import json
import pathlib
from typing import Any

import gspread
import pandas
import requests
from celery import shared_task, chain
from celery.utils.log import get_task_logger
from django.core.cache import cache
from django.core.files.base import ContentFile
from tabledocuments.logic.edit import load_document_by_url
from tabledocuments.logic.utils import (create_column_options,
                                        create_column_type_options)
from tabledocuments.models import TableDocument

logger = get_task_logger(__name__)


@shared_task
def update_document_options(document_uuid: str):
    """A trigger that gets fired once the document is created. It fixes
    traditional elements such as the columns the document encoding references
    the column names etc"""
    try:
        document = TableDocument.objects.get(document_uuid=document_uuid)
    except TableDocument.DoesNotExist:
        logger.error(f"Document with UUID {document_uuid} does not exist.")
        return

    if document.file is not None:
        try:
            path = pathlib.Path(document.file.path)
        except:
            logger.error(
                f"Document with UUID {document_uuid} "
                "has no file associated."
            )
        else:
            if path.exists() and path.is_file():
                try:
                    df = pandas.read_csv(path)
                except Exception as e:
                    logger.error(f'Failed to load document: {e}')
                    return None
                else:
                    column_type_options = create_column_type_options(
                        df.columns.tolist())
                    column_options = create_column_options(df.columns.tolist())

                try:
                    document = TableDocument.objects.get(
                        document_uuid=document_uuid)
                except TableDocument.DoesNotExist:
                    logger.error(
                        f"Document with UUID {document_uuid} does not exist.")
                else:
                    document.column_types = column_type_options
                    document.column_options = column_options
                    document.column_names = df.columns.tolist()
                    document.save()
                    logger.warning(
                        f"Successfully updated document options: {document.name}")


@shared_task
def get_document_from_url(url: str, headers: dict[str, str] = {}):
    """Task used to load the content of document returned via an API endpoint
    as a json format. The content will be loaded and transformed back to a csv
    database file"""
    async def proxy_get_url():
        response, errors = await load_document_by_url(url, headers=headers)

        if response.status_code != 200:
            logger.error(
                f"Failed to retrieve document from {url}, "
                f"status code: {response.status_code}"
            )
            return

        if errors:
            logger.error(
                f"Errors occurred while loading document from {url}: {errors}")
            return {'error': errors}

        if response is not None:
            if 'application/json' in response.headers.get('Content-Type', ''):
                logger.warning(
                    f"Successfully retrieved JSON document from {url}")
                return response.json()

            if 'text/csv' in response.headers.get('Content-Type', ''):
                logger.warning(
                    f"Successfully retrieved CSV document from {url}")
                return response.content.decode('utf-8-sig')
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
        # If data is a string, we suspect that it can
        # be csv content
        if isinstance(data, str):
            clean_data = list(csv.reader(data.splitlines(), delimiter=','))

            first_item = clean_data[0][-1]
            if ';' in first_item:
                clean_data = list(csv.reader(data.splitlines(), delimiter=';'))

            headers = clean_data.pop(0)
            df = pandas.DataFrame(clean_data, columns=headers)
            csv_content = df.to_csv(
                index=True, index_label='record_id', encoding='utf-8', doublequote=True)

            content = ContentFile(csv_content)
            document.file.save(f'{document.name}.csv', content)
            return

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
                logger.error(
                    f'Entry key {entry_key} not found '
                    f'in data: {string_data[:100]}...'
                )
                return

        if isinstance(data, list):
            # file = df.to_feather(index=True, index_label='record_id')
            # document.file.save(f'{document.name}.feather', file)

            df = pandas.DataFrame(data)
            csv_content = df.to_csv(
                index=True, index_label='record_id', encoding='utf-8', doublequote=True)
            content = ContentFile(csv_content)
            document.file.save(f'{document.name}.csv', content)

        document.save()
        logger.warning(
            f"Successfully created Feather document: {document.name}")


@shared_task
def load_google_sheet(api_key: str, sheet_id: str, range: str = None) -> str:
    """Loads data from a public Google Sheet using an API key and sheet ID."""
    instance = gspread.api_key(api_key)
    sheet = instance.open_by_key(sheet_id)

    # data = sheet.values_get(range or 'A1:B2')

    # sheet.sheet1.add_cols(1)
    # sheet.sheet1.update('C1', 'New Column')

    # values = data['values']
    # headers = values.pop(0)

    # df = pandas.DataFrame(values, columns=headers)
    # return df.to_csv(index=True, index_label='record_id', encoding='utf-8', doublequote=True)


@shared_task
def load_google_sheet_via_service_account(credentials: dict[str, str], sheet_id: str) -> str:
    """Loads data from a public Google Sheet using a service account and sheet ID.
    Reference: https://docs.gspread.org/en/latest/oauth2.html#service-account
    """
    instance = gspread.service_account_from_dict(credentials)
    sheet = instance.open_by_key(sheet_id)
    sheet.sheet1.insert_cols([['record_id']], 1)

    headers = sheet.sheet1.row_values(1)
    records = sheet.sheet1.get_all_records()
    cache.set(sheet_id, [headers, records], timeout=3600)

    df = pandas.DataFrame(records, columns=headers)
    return df.to_csv(index=False, encoding='utf-8', doublequote=True)


@shared_task
def merge_dataframes(document_uuid: str, data_to_append: str):
    buffer1 = io.StringIO(data_to_append)

    df1 = pandas.read_csv(buffer1)

    try:
        document = TableDocument.objects.get(document_uuid=document_uuid)
    except:
        logger.error(f'Failed to get document with UUID {document_uuid}')
        return

    df2 = pandas.read_csv(document.file.path)

    # 1. Run the before insert functions here on df1

    # 2. Merge the dataframes
    merged = pandas.concat([df1, df2], ignore_index=True)
    
    # 3. Run after insert functions here on merged

    # 4. Update the content of the physical file
    csv_content = merged.to_csv(index=False, encoding='utf-8', doublequote=True)
    content = ContentFile(csv_content)

    # 5. Sync the saved data with the database
    # providers if required

    document.file.save(f'{document.name}.csv', content)
    return content
