import enum
import json
from typing import Any

import numpy
import pandas
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from tabledocuments.validation_models import ColumnTypes


class WebsocketActions(enum.Enum):
    LOAD_VIA_ID = 'load_via_id'
    CHECKOUT_URL = 'checkout_url'


def upload_file_to(instance, filename):
    timesptamp = timezone.now().timestamp()
    extension = filename.split('.')[-1]
    new_filename = f"doc--{instance.document_uuid}__{timesptamp}.{extension}"
    return f"table_documents/{new_filename}"


def validate_file(name):
    """We only accept csv, xls, xlsx and ods files. We
    also allow json files but they will be transformed
    back to a csv format"""
    validator = FileExtensionValidator(
        allowed_extensions=['csv', 'xls', 'xlsx', 'ods', 'json'])
    validator(name)


def create_dataframe(clean_data: Any, column_options: list[dict[str, str | bool]]):
    """Create a pandas dataframe from the cleaned data
    after applying the column options such as renaming,
    filtering visible columns, enforcing unique columns"""

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

    all_column_names = list(
        map(
            lambda x: x['name'],
            column_options
        )
    )

    # Create the dataframe with the original
    # column names that will be renamed later
    df = pandas.DataFrame(
        clean_data,
        columns=all_column_names
    )

    for column in column_options:
        if column['columnType'] == ColumnTypes.STRING.value:
            df[column['name']] = df[column['name']].astype(str)
        elif column['columnType'] == 'Number':
            df[column['name']] = df[column['name']].astype(numpy.int64)
        elif column['columnType'] == 'Boolean':
            df[column['name']] = df[column['name']].apply(
                boolean_converter)
        elif column['columnType'] == 'Array' or column['columnType'] == 'Dict':
            df[column['name']] = df[column['name']].map(json_converter)

    # Resolve column name change
    renamed_columns = {}
    for col in column_options:
        new_name = col['newName']
        if new_name is None:
            continue

        renamed_columns[col['name']] = new_name
    
    if renamed_columns:
        df = df.rename(columns=renamed_columns)

    visible_columns = list(
        filter(
            lambda x: x['visible'],
            column_options
        )
    )

    # Resolve fields with "null" values
    none_nullable_columns = list(
        filter(
            lambda x: not x['nullable'],
            visible_columns
        )
    )
    none_nullable_columns_names = list(
        map(
            lambda x: x['newName'],
            none_nullable_columns
        )
    )

    if none_nullable_columns:
        df = df.dropna(subset=none_nullable_columns_names)

    # Resolve unique data in each columns
    unique_columns = list(
        filter(
            lambda x: x['unique'],
            visible_columns
        )
    )
    unique_columns_names = list(
        map(
            lambda x: x['newName'] or x['name'],
            unique_columns
        )
    )

    if unique_columns:
        df.drop_duplicates(
            subset=unique_columns_names,
            inplace=True
        )

    # Resolve hidden/unhidden columns
    visible_columns = list(
        filter(
            lambda x: x['visible'],
            column_options
        )
    )
    visible_column_names = list(
        map(
            lambda x: x['newName'] or x['name'],
            visible_columns
        )
    )

    if visible_column_names:
        df = df[visible_column_names]

    return df
