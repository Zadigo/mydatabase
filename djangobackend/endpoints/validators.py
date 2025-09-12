from django.core.exceptions import ValidationError


def validate_http_method(value: list[str]):
    valid_methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']

    for item in value:
        if item not in valid_methods:
            raise ValidationError(
                f"{item} is not a valid HTTP method. Choose from {valid_methods}"
            )
