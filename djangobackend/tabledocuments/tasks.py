import csv
import io
import json
from typing import Any

import gspread
import pandas
from asgiref.sync import async_to_sync
from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.cache import cache
from django.core.files.base import ContentFile
from gspread.utils import rowcol_to_a1
from tabledocuments.logic.edit import DocumentEdition
from tabledocuments.models import TableDocument
from tabledocuments.utils import create_dataframe

logger = get_task_logger(__name__)


@shared_task
def update_document_options(document_uuid: str, column_options: list[dict[str, str | bool]] = [], from_file: bool = False):
    """A trigger that gets fired once the document is created. It fixes
    elements such as the columns, the document encoding references,
    the column names, etc."""
    try:
        document = TableDocument.objects.get(document_uuid=document_uuid)
    except TableDocument.DoesNotExist:
        logger.error(f"Document with UUID {document_uuid} does not exist.")
        return

    # if from_file and document.file is not None:
    #     df = pandas.read_csv(document.file.path)

    document.column_options = column_options
    document.column_names = list(
        map(
            lambda x: x['newName'] or x['name'], 
            column_options
        )
    )

    column_types = {}
    for item in column_options:
        column_name = item['newName'] or item['name']
        column_types[column_name] = item['columnType']

    document.column_types = column_types
    document.save()

    logger.warning(
        f"Successfully updated document options for document: {document.name}"
    )


@shared_task
def create_csv_file_from_data(data: Any, document_id: str | int, entry_key: str | None = None, column_options: list[dict[str, Any]] = []):
    """Creates a CSV file from the provided data which can be either
    a string (CSV content), a list of records (JSON content) or
    a dictionary containing the data under a specific entry key. The
    created CSV file is then saved to the TableDocument instance
    identified by document_id.
    
    Args:
        data: The input data which can be a CSV string, a list of records, or a dictionary.
        document_id: The ID of the TableDocument instance to which the file will be saved.
        entry_key: If data is a dictionary, this key is used to extract the relevant data.
        column_options: A list of dictionaries containing column options such as name and type.
    """
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
        if isinstance(data, bytes):
            data = data.decode('utf-8-sig')

        if isinstance(data, str):
            clean_data = list(csv.reader(data.splitlines(), delimiter=','))
            
            first_item = clean_data[0][-1]
            if ';' in first_item:
                clean_data = list(csv.reader(data.splitlines(), delimiter=';'))
            breakpoint()
            df = create_dataframe(clean_data[1:], column_options)
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

            df = create_dataframe(data, column_options)
            csv_content = df.to_csv(**df_params)

            content = ContentFile(csv_content)
            document.file.save(f'{document.name}.csv', content)

            document.save()
            logger.warning(
                "Successfully created Feather "
                f"document from list/json: {document.name}"
            )

    # Once the document is created, we need to populate
    # column_options, column_types and column_names
    update_document_options.apply_async(
        args=[
            str(document.document_uuid),
            column_options
        ],
        countdown=10
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

    logger.warning(
        f'Successfully retrieved data from Google Sheet: {sheet_id}')

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


@shared_task
def get_document_from_url(url: str, headers: dict[str, str] = {}):
    """Task used to load the content of document returned via an API endpoint
    as a json format. The content will be loaded and transformed back to a csv
    database file"""
    instance = DocumentEdition()
    document = async_to_sync(
        instance.load_json_document_by_url
    )(url, headers=headers)
    logger.warning(f"Successfully retrieved document from {url}")
