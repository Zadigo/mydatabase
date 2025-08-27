def validate_http_method(value: str):
    valid_methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']
    
    methods = value.split(',')
    for method in methods:
        if method not in valid_methods:
            raise ValidationError(
                f"{method} is not a valid HTTP method. Choose from {valid_methods}."
            )
