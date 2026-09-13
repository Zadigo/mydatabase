from collections.abc import Sequence
from typing import Any

from pydantic import BaseModel

from tabledocuments.validation_models import ColumnOptionsModel


def create_column_options(columns: Sequence[str]):
    """Function that creates column options that is used
    in the frontend to toggle visibility, editability or
    other functionalities on specific given columns"""
    return [
        ColumnOptionsModel(name=column)
        for column in columns
    ]


def create_column_options_from_dict(columns: Sequence[dict[str, Any]]):
    return [ColumnOptionsModel(**column) for column in columns]


def resolve_models[T = BaseModel](models: Sequence[T]) -> list[dict[str, Any]]:
    """Function that resolves a sequence of Pydantic models into dictionaries"""
    return [model.model_dump() for model in models]


def user_preference_column_options(columns: Sequence[str]):
    """Function that creates column options that the user can
    set as preferences for the final table presentation. This is used
    when the user wants to save their preferences for a given document"""
    result = create_column_options(columns)

    options = []
    for item in result:
        item.update(visible=True)
        options.append(item)
    return options
