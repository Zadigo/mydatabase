from typing import Literal

from pydantic import BaseModel, Field


class DocumentInfoModel(BaseModel):
    uuid: str = Field(...)
    name: str = Field(...)


class WsMessageModel(BaseModel):
    action: str | None = Field(default=None)
    document: DocumentInfoModel | None = Field(...)
    table_id: str | None = Field(...)
    document_uuid: str | None = Field(default=None)


class _LoadedViaIdColumns(BaseModel):
    names: list[str] = Field(...)
    options: list[str] = Field(...)
    types: list[str] = Field(...)
    type_options: list[str] = Field(...)


class LoadViaIdModel(WsMessageModel):
    document_data: str = Field(...)
    columns: list[_LoadedViaIdColumns] = Field(...)


class ColumnTypeOptions(BaseModel):
    name: str = Field(...)
    newName: str = Field(...)
    columnType: Literal['String'] = Field(default='String')
    unique: bool = Field(default=False)
    nullable: bool = Field(default=True)


class CreateColumnOptions(BaseModel):
    name: str = Field(...)
    visible: bool = Field(default=True)
    editable: bool = Field(default=True)
    sortable: bool = Field(default=True)
    searchable: bool = Field(default=True)
