import re

from rest_framework.exceptions import ValidationError


def slide_data_source_validator(value):
    result = re.match(r'ds_[a-zA-Z0-9]{5}', value)
    if not result:
        raise ValidationError({
            'slide_data_source': 'Data source is not a valid format'
        })
