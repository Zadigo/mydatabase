import re

from django.core.exceptions import ValidationError


def validate_id(value):
    """Validates the IDs created in the database"""
    result = re.match(r'^(sh|bl|wk|pg)_[a-zA-Z0-9]{5}$', value)
    if not result:
        raise ValidationError('Data source id is not valid')
