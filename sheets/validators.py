import re

from django.core.exceptions import ValidationError


def validate_id(value):
    """Validates the IDs created in the database"""
    result = re.match(r'^(sh|bl|wk|pg)_[a-zA-Z0-9]{5}$', value)
    if not result:
        raise ValidationError('Sheet id is not valid')


def validate_text_length(value):
    result = re.match(r'\w+\s+', value)
    if not result:
        raise ValidationError({'name': 'Is not a valid text'})
