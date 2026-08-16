import csv
import datetime
import json
from typing import Any

import gspread
import httpx2
import pandas
import pytz
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db.models import QuerySet
from django.utils.crypto import get_random_string
from gspread.exceptions import APIError
from gspread.utils import rowcol_to_a1

from dbschemas.models import DatabaseProvider
from djangobackend.huey_app import huey_task
from tabledocuments.logic.utils import (
    clean_user_column_type_options,
    create_column_options,
    create_column_type_options,
)
from tabledocuments.models import TableDocument
from tabledocuments.utils import Document
from tabledocuments.utils.constants import DOCUMENT_CACHE_KEY_PREFIX
from tabledocuments.utils.file_manipulation import create_dataframe


@huey_task.task(retries=3, retry_delay=10, timeout=60, priority=10)
def update_document_options(document_uuid: str, column_type_options: list[dict[str, str | bool]] | None = None, from_file: bool = False):
    """A trigger that gets fired once the document is created. It fixes
    elements such as the columns, the document# encoding references,
    the column names, etc."""
    try:
        document = TableDocument.objects.get(document_uuid=document_uuid)
    except TableDocument.DoesNotExist:
        # logger.error(f"Document with UUID {document_uuid} does not exist.")
        return

    # If the task is triggered from the admin interface, then we need to
    # load the document from the file to update the column options
    # based on the content of the file. Otherwise, we can directly use the
    # column options provided as arguments when the task is triggered from Nuxt
    if from_file and document.file is not None:
        df = pandas.read_csv(document.file.path)
        column_type_options = create_column_type_options(df.columns.tolist())

    document.column_type_options = clean_user_column_type_options(column_type_options)
    document.column_names = [
        x['newName'] or x['name']
            for x in document.column_type_options
    ]

    column_types = {}
    for item in document.column_type_options:
        column_name = item['newName'] or item['name']
        column_types[column_name] = item['columnType']

    document.column_types = column_types

    column_options = create_column_options(document.column_names)
    document.column_options = column_options
    document.save()

    # logger.warning(
    #     f"Successfully updated document options for document: {document.name}"
    # )


@huey_task.task(retries=3, retry_delay=10, timeout=60, priority=90)
@huey_task.rate_limit('create_csv_file_from_data', 100, 60)
def create_csv_file_from_data(data: Any, document_id: str | int, column_type_options: list[dict[str, Any]] | None = None):
    if data is None or data == '':
        # logger.warning(f'No data provided? Received {data}')
        return

    df_params = {
        'index': True,
        'header': True,
        'index_label': 'record_id',
        'encoding': 'utf-8',
        'doublequote': True
    }

    try:
        document = TableDocument.objects.get(id=document_id)
    except TableDocument.DoesNotExist:
        # logger.error(f"Document with ID {document_id} does not exist.")
        return
    else:
        if isinstance(data, bytes):
            data = data.decode('utf-8-sig')

        if isinstance(data, str):
            clean_data = list(csv.reader(data.splitlines(), delimiter=','))
            
            first_item = clean_data[0][-1]
            if ';' in first_item:
                clean_data = list(csv.reader(data.splitlines(), delimiter=';'))

            df = create_dataframe(clean_data[1:], column_type_options)
            csv_content = df.to_csv(**df_params)

            content = ContentFile(csv_content)
            document.file.save(f'{document.name}.csv', content)
            document.save()
            
            # logger.warning(
            #     "Successfully created Feather "
            #     f"document from csv string: {document.name}"
            # )

        # Once the document is created, we need to populate
        # column_options, column_types and column_names
        t1 = update_document_options.s(str(document.document_uuid), column_type_options)
        huey_task.enqueue(t1)


@huey_task.task(retries=3, retry_delay=10, timeout=60, priority=90)
@huey_task.rate_limit('create_json_file_from_data', 100, 60)
def create_json_file_from_data(data: Any, document_id: str | int, entry_key: str | None = None, column_type_options: list[dict[str, Any]] = []):
    if data is None or data == '':
        # logger.warning(f'No data provided? Received {data}')
        return
    
    df_params = {
        'index': True,
        'header': True,
        'index_label': 'record_id',
        'encoding': 'utf-8',
        'doublequote': True
    }

    try:
        document = TableDocument.objects.get(id=document_id)
    except TableDocument.DoesNotExist:
        # logger.error(f"Document with ID {document_id} does not exist.")
        return
    else:
        if isinstance(data, dict):
            if entry_key is None:
                string_data = json.dumps(data)
                # logger.error(
                #     'Object is a dictionnary and no '
                #     f'entry key was provided: {string_data[:100]}...'
                # )
                return

            if 'error' in data:
                return data

            try:
                data = data[entry_key]
            except KeyError:
                string_data = json.dumps(data)
                # logger.error(
                #     f'Entry key {entry_key} not found '
                #     f'in data: {string_data[:100]}...'
                # )
                return

        if isinstance(data, list):
            df = create_dataframe(data, column_type_options)
            csv_content = df.to_csv(**df_params)

            content = ContentFile(csv_content)
            document.file.save(f'{document.name}.csv', content)
            document.save()

            # logger.warning(
            #     "Successfully created Feather "
            #     f"document from list/json: {document.name}"
            # )

       # Once the document is created, we need to populate
        # column_options, column_types and column_names
        t1 = update_document_options.s(str(document.document_uuid), column_type_options)
        huey_task.enqueue(t1)


@huey_task.task(retries=3, retry_delay=10, timeout=60, priority=90)
@huey_task.rate_limit('create_csv_from_google_sheet', 100, 60)
def create_csv_from_google_sheet(table_id: int, sheet_id: str) -> str:
    """Loads data from a Google Sheet using a service account and sheet ID and
    returns the values as string.
    
    https://docs.gspread.org/en/latest/oauth2.html#service-account

    Args:
        credentials (dict): A dictionary containing the service account credentials.
        sheet_id (str): The ID of the Google Sheet to retrieve data from.
    """
    try:
        table = TableDocument.objects.get(id=table_id)
    except TableDocument.DoesNotExist:
        # logger.error(f"TableDocument with ID {table_id} does not exist.")
        return
    else:
        providers: QuerySet[DatabaseProvider] = table.database_schema.databaseprovider_set.all()
        if providers.exists():
            try:
                provider = providers.get(has_google_sheet_connection=True)
            except DatabaseProvider.DoesNotExist:
                raise ValidationError(
                    'No provider with Google Sheet connection found')

            # Attacj the crendtials to the provider for use with gspread
            instance = gspread.service_account_from_dict(provider.google_sheet_credentials)

            try:
                sheet = instance.open_by_key(sheet_id)
            except APIError:
                # logger.error(f'Failed to open spreadsheet: {e}')
                return

            headers = sheet.sheet1.row_values(1)
            records = sheet.sheet1.get_all_records()
            cache.set(sheet_id, [headers, records], timeout=3600)

            if 'record_id' not in headers:
                sheet.sheet1.insert_cols([['record_id']], 1)

                # Create the auto-incrementing record_id column
                cell_name = 'A2:' + rowcol_to_a1(len(records) + 1, 1)
                cell_list = sheet.sheet1.range(cell_name)

                for i, cell in enumerate(cell_list):
                    cell.value = i + 1

                sheet.sheet1.update_cells(cell_list)

            # logger.warning(
            #     f'Successfully retrieved data from Google Sheet: {sheet_id}')

            df = pandas.DataFrame(records, columns=headers)
            return df.to_csv(index=False, encoding='utf-8', doublequote=True)


@huey_task.task(retries=3, retry_delay=10, timeout=60, priority=90)
@huey_task.rate_limit('prefetch_data_from_url', 100, 30)
def prefetch_data_from_url(url: str, **params):
    with httpx2.Client(url) as client:
        try:
            response = client.get(url, **params)
            response.raise_for_status()
        except httpx2.RequestError as e:
            return None, [str(e)]
        else:
            if response.status_code != 200:
                return None, [f"Failed to load document. Status code: {response.status_code}"]

            return response, []


@huey_task.task(retries=3, retry_delay=10, timeout=60, priority=90)
@huey_task.rate_limit('create_csv_from_google_sheet', 100, 60)
def create_csv_from_url(url: str, headers: dict[str, str] = {}) -> tuple[str, dict | list]:
    """Task used to load the content of document returned via an API endpoint
    as a json format. The content will be loaded and transformed back to a csv
    database file
    
    Args:

    """
    data, errors = prefetch_data_from_url(url, headers=headers)
 
    if errors is not None:
        pass 

    df = create_dataframe(data)

    date = str(datetime.datetime.now(tz=pytz.UTC))
    cache_key = DOCUMENT_CACHE_KEY_PREFIX.format(name=get_random_string(length=10))
    document = Document(cache_key, df, metadata={'url': url, 'date': date})
    # Convert the content of the dataframe to a CSV content
    str_data = document.content.to_csv(index=False, encoding='utf-8', doublequote=True)

    name = get_random_string(8)
    content_file = ContentFile(str_data, name=f'{cache_key}.csv')

    # Create the document
    instance = TableDocument.objects.create(name=name)
    instance.file = content_file
    instance.url = url
    instance.save()

    update_document_options.schedule(
        args=(
            str(instance.document_uuid),
            create_column_options(document.content.columns.tolist())
        ),
        delay=20,
        priority=50
    )

    return cache_key, data
    
    # logger.warning(f"Successfully create file: {name}")
