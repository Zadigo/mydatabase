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
    name: str = Field(...)
    newName: str | None = Field(default=None)
    columnType: Literal['String', 'Number', 'Boolean', 'Array', 'Dict'] = Field(default='String')
    visible: bool = Field(default=True)
    editable: bool = Field(default=True)
    sortable: bool = Field(default=True)
    searchable: bool = Field(default=True)
    nullable: bool = Field(default=True)
    unique: bool = Field(default=False)


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
