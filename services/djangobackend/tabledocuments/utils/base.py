from typing import Any


def resolve_entry_key[T = dict[str, Any]](value: str, data: T) -> T:
    """Resolve the entry key in a dictionary and return the value."""
    if not value or value == '':
        return data

    keys = value.split('.')
    for key in keys:
        data = data.get(key, {})
    return data
