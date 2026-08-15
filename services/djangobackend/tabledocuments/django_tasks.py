import csv
from typing import Any

import pandas
from django.core.files.base import ContentFile

from djangobackend.huey_app import huey_task
from tabledocuments.logic.utils import (
    clean_user_column_type_options,
    create_column_options,
    create_column_type_options,
)
from tabledocuments.models import TableDocument
from tabledocuments.utils import create_dataframe


@huey_task.task(retries=3, retry_delay=10, timeout=60)
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


@huey_task.task(retries=3, retry_delay=10, timeout=60)
@huey_task.rate_limit('update_document_options', 100, 60)
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
