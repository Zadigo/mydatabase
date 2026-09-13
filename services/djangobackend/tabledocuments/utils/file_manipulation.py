import json
from collections.abc import Sequence
from typing import Any

import numpy
import pandas

from tabledocuments.validation_models import ColumnOptionsModel, ColumnTypes


def is_csv_file(name: str):
    """Check if the file is a CSV file based on its extension"""
    return name.endswith('.csv')

def is_json_file(name: str):
    """Check if the file is a JSON file based on its extension"""
    return name.endswith('.json')


def create_dataframe(clean_data: list[dict[str, Any]], column_options: Sequence[ColumnOptionsModel]):
    """Create a pandas dataframe from the cleaned data
    after applying the column options such as renaming,
    filtering visible columns, enforcing unique columns
    
    Args:
        clean_data (list[dict[str, Any] | list[Any]]): The cleaned data to create the dataframe from.
        column_options (Sequence[ColumnOptionsModel]): The column options to apply to the dataframe.

    Returns:
        pandas.DataFrame: The created dataframe after applying the column options.
    """
    def boolean_converter(value):
        if value is None:
            return value

        true_values = ['1', 'true', True]
        return value in true_values

    def json_converter(value):
        if value is None:
            return value

        try:
            return str(json.loads(value))
        except Exception:
            return value

    

    # Create the dataframe with the original
    # column names that will be renamed later
    column_names = [x.name for x in column_options]
    df = pandas.DataFrame(clean_data, columns=column_names)

    # For each column, apply the type 
    # conversion based on the column options
    for column in column_options:
        item_series = df[column.name]

        if column.columnType == ColumnTypes.STRING.value:
            df[column.name] = item_series.astype(str)
        elif column.columnType == ColumnTypes.NUMBER.value:
            df[column.name] = item_series.astype(numpy.int64)
        elif column.columnType == ColumnTypes.BOOLEAN.value:
            df[column.name] = item_series.apply(boolean_converter)
        elif column.columnType == ColumnTypes.ARRAY.value or column.columnType == ColumnTypes.DICT.value:
            df[column.name] = item_series.map(json_converter)

    # Resolve column name change
    renamed_columns = {}
    for col in column_options:
        if col.newName is None:
            continue

        renamed_columns[col.name] = col.newName
    
    if renamed_columns:
        df = df.rename(columns=renamed_columns)

    visible_columns = list(
        filter(
            lambda x: x.visible,
            column_options
        )
    )

    # Resolve fields with "null" values
    none_nullable_columns = list(
        filter(
            lambda x: not x.nullable,
            visible_columns
        )
    )
    none_nullable_columns_names = [x.newName or x.name for x in none_nullable_columns]

    if none_nullable_columns:
        df.dropna(subset=none_nullable_columns_names, inplace=True)

    # Resolve unique data in each columns
    unique_columns = list(
        filter(
            lambda x: x.unique,
            visible_columns
        )
    )
    unique_columns_names = [x.newName or x.name for x in unique_columns]

    if unique_columns:
        df.drop_duplicates(
            subset=unique_columns_names,
            inplace=True
        )

    # Resolve hidden/unhidden columns
    visible_columns = list(
        filter(
            lambda x: x.visible,
            column_options
        )
    )
    visible_column_names = [x.newName or x.name for x in visible_columns]

    if visible_column_names:
        df = df[visible_column_names]

    return df
