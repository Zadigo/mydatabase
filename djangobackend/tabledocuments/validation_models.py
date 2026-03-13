from pydantic.fields import Field
from pydantic import BaseModel
from typing import Annotated
import enum


class ColumnTypes(enum.Enum):
    STRING = 'String'
    NUMBER = 'Number'
    BOOLEAN = 'Boolean'
    ARRAY = 'Array'
    DICT = 'Dict'


class ColumnOption(BaseModel):
    name: str
    newName: str = None
    columnType: Annotated[ColumnTypes, Field(default=ColumnTypes.STRING.value)]
    visible: Annotated[bool, Field(default=True)]
    editable: Annotated[bool, Field(default=True)]
    sortable: Annotated[bool, Field(default=True)]
    searchable: Annotated[bool, Field(default=True)]
    nullable: Annotated[bool, Field(default=True)]
    unique: Annotated[bool, Field(default=False)]


class ColumnTypeOptions(BaseModel):
    name: str
    columnType: Annotated[ColumnTypes, Field(default=ColumnTypes.STRING.value)]
    unique: Annotated[bool, Field(default=False)]
    nullable: Annotated[bool, Field(default=True)]
