import asyncio
import csv
import io
import json
import pathlib
from typing import Any

import gspread
import numpy
import pandas
import requests
from celery import chain, shared_task
from celery.utils.log import get_task_logger
from django.core.cache import cache
from django.core.files.base import ContentFile
from gspread.utils import TableDirection, rowcol_to_a1
from tabledocuments.logic.edit import load_document_by_url
from tabledocuments.logic.utils import (create_column_options,
                                        create_column_type_options)
from tabledocuments.models import TableDocument

logger = get_task_logger(__name__)


@shared_task
def update_document_options(document_uuid: str, column_type_options: list[dict[str, Any]] = []):
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
                    document = TableDocument.objects.get(
                        document_uuid=document_uuid
                    )
                except TableDocument.DoesNotExist:
                    logger.error(
                        f"Document with UUID {document_uuid} "
                        "does not exist."
                    )

                try:
                    df = pandas.read_csv(path)
                except Exception as e:
                    logger.error(f'Failed to load document: {e}')
                    return None
                else:
                    if column_type_options:
                        document.column_types = column_type_options
                    else:
                        document.column_types = create_column_type_options(
                            df.columns.tolist())

                    document.column_options = create_column_options(
                        df.columns.tolist())
                    document.column_names = df.columns.tolist()
                    document.save()

                    logger.warning(
                        "Successfully updated "
                        f"document options: {document.name}"
                    )


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
def create_csv_file_from_data(data: Any, document_id: str | int, entry_key: str | None = None, column_options: list[dict[str, Any]] = []):
    if data is None or data == '':
        logger.warning(f'No data provided? Received {data}')
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
        logger.error(f"Document with ID {document_id} does not exist.")
        return
    else:
        all_column_names = list(
            map(
                lambda x: x['name'],
                column_options
            )
        )

        renamed_columns = {}
        for col in column_options:
            renamed_columns[col['name']] = col['new_name']

        visible_columns = list(
            filter(
                lambda x: x['visible'],
                column_options
            )
        )
        visible_column_names = list(
            map(
                lambda x: x['new_name'],
                visible_columns
            )
        )

        unique_columns = list(
            filter(lambda x: x['unique'],
                   visible_columns
                   )
        )
        unique_columns_names = list(
            map(
                lambda x: x['new_name'],
                unique_columns
            )
        )
        none_nullable_columns = list(
            filter(
                lambda x: not x['nullable'],
                visible_columns
            )
        )
        none_nullable_columns_names = list(
            map(
                lambda x: x['new_name'],
                none_nullable_columns
            )
        )

        def boolean_converter(value):
            if value is None:
                return value

            true_values = ['1', 'true', True]
            if value in true_values:
                return True
            return False

        def json_converter(value):
            if value is None:
                return value

            try:
                data = json.loads(value)
            except:
                return value
            return str(data)

        def create_dataframe(clean_data):
            df = pandas.DataFrame(
                clean_data,
                columns=all_column_names
            )

            for column in column_options:
                if column['columnType'] == 'String':
                    df[column['name']] = df[column['name']].astype(str)
                elif column['columnType'] == 'Number':
                    df[column['name']] = df[column['name']].astype(numpy.int64)
                elif column['columnType'] == 'Boolean':
                    df[column['name']] = df[column['name']].apply(boolean_converter)
                elif column['columnType'] == 'Array' or column['columnType'] == 'Dict':
                    df[column['name']] = df[column['name']].map(json_converter)

            df = df.rename(columns=renamed_columns)

            if none_nullable_columns:
                df = df.dropna(subset=none_nullable_columns_names)

            if unique_columns:
                df.drop_duplicates(
                    subset=unique_columns_names,
                    inplace=True
                )

            if visible_column_names:
                df = df[visible_column_names]

            return df

        data = data.decode('utf-8-sig')

        if isinstance(data, str):
            clean_data = list(csv.reader(data.splitlines(), delimiter=','))
            first_item = clean_data[0][-1]
            if ';' in first_item:
                clean_data = list(csv.reader(data.splitlines(), delimiter=';'))

            df = create_dataframe(clean_data[1:])
            csv_content = df.to_csv(**df_params)

            content = ContentFile(csv_content)
            document.file.save(f'{document.name}.csv', content)
            document.save()
            logger.warning(
                "Successfully created Feather "
                f"document from csv string: {document.name}"
            )

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

            df = create_dataframe(data)
            csv_content = df.to_csv(**df_params)

            content = ContentFile(csv_content)
            document.file.save(f'{document.name}.csv', content)

            document.save()
            logger.warning(
                "Successfully created Feather "
                f"document from list/json: {document.name}"
            )


@shared_task
def get_document_from_public_google_sheet(api_key: str, sheet_id: str, range: str = None) -> str:
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
def get_document_from_google_sheet(credentials: dict[str, str], sheet_id: str) -> str:
    """Loads data from a Google Sheet using a service account and sheet ID and
    returns the values as string
    Reference: https://docs.gspread.org/en/latest/oauth2.html#service-account
    """
    instance = gspread.service_account_from_dict(credentials)

    try:
        sheet = instance.open_by_key(sheet_id)
    except Exception as e:
        logger.error(f'Failed to open spreadsheet: {e}')


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

    logger.warning(f'Successfully retrieved data from Google Sheet: {sheet_id}')

    df = pandas.DataFrame(records, columns=headers)
    return df.to_csv(index=False, encoding='utf-8', doublequote=True)


@shared_task
def append_to_dataframe(document_uuid: str, data_to_append: str):
    """Function used to append data to an existing document. The data
    to append is provided as a CSV string. The function will load the existing
    document, merge the data and save it back to the file.
    ### 1. Load the data to append into a dataframe
    ### 2. Load the existing document into a dataframe
    """
    buffer1 = io.StringIO(data_to_append)

    df1 = pandas.read_csv(buffer1)

    try:
        document = TableDocument.objects.get(document_uuid=document_uuid)
    except:
        logger.error(f'Failed to get document with UUID {document_uuid}')
        return

    df2 = pandas.read_csv(document.file.path)

    # If the documents do not have the same columns,
    # then do not try to append the documents
    if df1.columns.tolist() != df2.columns.tolist():
        logger.warning('Columns mismatch')
        return

    # 1. Run the before insert functions here on df1

    # 2. Merge the dataframes
    merged = pandas.concat([df1, df2], ignore_index=True)

    # 3. Run after insert functions here on merged

    # 4. Update the content of the physical file
    csv_content = merged.to_csv(
        index=False, 
        encoding='utf-8', 
        doublequote=True
    )
    content = ContentFile(csv_content)

    # 5. Sync the saved data with the database
    # providers if required

    document.file.save(f'{document.name}.csv', content)
    return content
