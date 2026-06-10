from django.core.exceptions import ValidationError
from pydantic import BaseModel, field_validator
from typing import Optional

def validate_http_method(value: list[str]):
    valid_methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']

    for item in value:
        if item not in valid_methods:
            raise ValidationError(
                f"{item} is not a valid HTTP method. Choose from {valid_methods}"
            )


class QueryValidator(BaseModel):
    select: Optional[str] = None
    where: Optional[str] = None
    order_by: Optional[str] = None
    offset: Optional[str] = None
    limit: Optional[str] = None

    @field_validator('offset', 'limit', mode='before')
    @classmethod
    def ensure_digit(cls, value: Optional[str]):
        if value is not None and not value.isdigit():
            raise ValueError(f"{value} is not a valid integer.")
        return value

    @field_validator('select')
    @classmethod
    def validate_select(cls, value: Optional[str]):
        if value is not None:
            if value == '*':
                return value
            
            # columns = [col.strip() for col in value.split(',')]
            # if not all(columns):
            #     raise ValueError("Select fields cannot be empty.")
        return value
