from django.core.exceptions import ValidationError
from pydantic import BaseModel, field_validator


def validate_http_method(value: list[str]):
    valid_methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']

    for item in value:
        if item not in valid_methods:
            raise ValidationError(
                f"{item} is not a valid HTTP method. Choose from {valid_methods}"
            )


class QueryValidator(BaseModel):
    select: str | None = None
    where: str | None = None
    order_by: str | None = None
    offset: str | None = None
    limit: str | None = None

    @field_validator('offset', 'limit', mode='before')
    @classmethod
    def ensure_digit(cls, value: str | None):
        if value is not None and not value.isdigit():
            raise ValueError(f"{value} is not a valid integer.")
        return value

    @field_validator('select')
    @classmethod
    def validate_select(cls, value: str | None):
        if value is not None and value == '*':
            return value
            
            # columns = [col.strip() for col in value.split(',')]
            # if not all(columns):
            #     raise ValueError("Select fields cannot be empty.")
        return value
