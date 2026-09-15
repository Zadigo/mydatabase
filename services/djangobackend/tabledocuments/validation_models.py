import enum
from typing import Literal

from pydantic import BaseModel, Field


class ColumnTypes(enum.Enum):
    STRING = 'String'
    NUMBER = 'Number'
    BOOLEAN = 'Boolean'
    ARRAY = 'Array'
    DICT = 'Dict'


class ColumnOptionsModel(BaseModel):
    """Model representing the options for a column in a table document.
    
    Attributes:
        name (str): The name of the column.
        newName (str | None): The new name of the column, if it is being renamed.
        columnType (Literal['String', 'Number', 'Boolean', 'Array', 'Dict']): The data type of the column.
        visible (bool): Whether the column is visible.
        editable (bool): Whether the column is editable.
        sortable (bool): Whether the column is sortable.
        searchable (bool): Whether the column is searchable.
        nullable (bool): Whether the column can contain null values.
        unique (bool): Whether the column values must be unique.
    """
    
    name: str = Field(...)
    newName: str | None = Field(default=None)
    columnType: Literal['String', 'Number', 'Boolean', 'Array', 'Dict'] = Field(default='String')
    visible: bool = Field(default=True)
    editable: bool = Field(default=True)
    sortable: bool = Field(default=True)
    searchable: bool = Field(default=True)
    nullable: bool = Field(default=True)
    unique: bool = Field(default=False)


class OptionalColumnOptionsModel(ColumnOptionsModel):
    """Model representing the options for a column in a table document 
    where all fields are optional."""

    name: str | None = Field(default=None)


class ColumnTypesModel(BaseModel):
    """Model representing the type of a column in a table document."""

    name: str = Field(...)
    columnType: Literal['String', 'Number', 'Boolean', 'Array', 'Dict'] = Field(default='String')


class DocumentInfoModel(BaseModel):
    uuid: str = Field(...)
    name: str = Field(...)


class LoadedViaIdColumns(BaseModel):
    names: list[str] = Field(...)
    options: list[dict[str, str | bool]] = Field(...)
    types: list[dict[str, str]] = Field(...)
    type_options: list[dict[str, str | bool]] = Field(...)


class WsMessageModel(BaseModel):
    action: str | None = Field(default=None)
    document: DocumentInfoModel | None = Field(...)
    table_id: str | None = Field(...)
    document_uuid: str | None = Field(default=None)
    document_data: str | None = Field(default=None)
    columns: list[LoadedViaIdColumns] = Field(default_factory=list)


class WsSendMessageModel(BaseModel):
    action: str = Field(...)
    document_data: str = Field(...)
    columns: LoadedViaIdColumns | None = Field(default=None)
