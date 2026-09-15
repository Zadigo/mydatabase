from collections.abc import Sequence

from tabledocuments.validation_models import ColumnTypesModel


def convert_to_types_models(raw_values: Sequence[dict[str, str]]):
    """A generator function that converts a sequence of raw dictionaries into ColumnTypesModel instances.
    
    .. code-block:: python

        raw_values = [
            {"name": "column1", "columnType": "String"},
            {"name": "column2", "columnType": "Number"},
        ]
        for model in convert_to_types_models(raw_values):
            print(model)
    """
    for item in raw_values:
        yield ColumnTypesModel(**item)
