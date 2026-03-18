from pydantic.fields import Field
from pydantic import BaseModel
from typing import Annotated, Optional
import enum


class ColumnTypes(enum.Enum):
    STRING = 'String'
    NUMBER = 'Number'
    BOOLEAN = 'Boolean'
    ARRAY = 'Array'
    DICT = 'Dict'


class ColumnOption(BaseModel):
    name: str
    newName: Optional[str] = None
    columnType: Annotated[ColumnTypes, Field(default=ColumnTypes.STRING.value)]
    unique: Annotated[bool, Field(default=False)]
    visible: Annotated[bool, Field(default=True)]
    nullable: Annotated[bool, Field(default=True)]
    editable: Annotated[bool, Field(default=True)]
    sortable: Annotated[bool, Field(default=True)]
    searchable: Annotated[bool, Field(default=True)]


class ColumnTypeOption(BaseModel):
    name: str
    columnType: Annotated[ColumnTypes, Field(default=ColumnTypes.STRING.value)]
    unique: Annotated[bool, Field(default=False)]
    nullable: Annotated[bool, Field(default=True)]


class MixedColumnOption(ColumnOption, ColumnTypeOption):
    """A validator that combines the options of ColumnOption
    and ColumnTypeOption. This is useful for endpoints that need to validate
    both sets of options simultaneously."""
