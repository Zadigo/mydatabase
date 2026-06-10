from django.utils.crypto import get_random_string

def create_endpoint(prefix: str) -> str:
    """Creates a unique endpoint identifier"""
    parts = [
        prefix,
        get_random_string(5),
        get_random_string(10)
    ]
    return '-'.join(parts)
