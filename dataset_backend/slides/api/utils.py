def list_manager(instance, field, value):
    """A manager for adding or appending values in
    the stored list values in the database"""
    result = getattr(instance, field, [])
    if len(result) == 0:
        result.append(value)
    else:
        if value in result:
            index_of_value = result.index(value)
            result.pop(index_of_value)
        else:
            result.append(value)
    setattr(instance, field, result)
    return instance


def list_remover(instance, field, value, request_value):
    """Removes a value to a list if a value from the request
    matches a given condition"""
    if not request_value:
        result = getattr(instance, field)
        index_of_value = result.index(value)
        result.pop(index_of_value)
        setattr(instance, field, result)
    return instance


def list_adder(instance, field, value, request_value):
    """Adds a value to a list if a value from the request
    matches a given condition"""
    if request_value:
        result = getattr(instance, field)
        result.append(value)
        setattr(instance, field, result)
    return instance


def create_true_false_dictionnaries(columns: list[str]):
    """Create list of True/False items using a list
    of columns as strings"""
    return [{'name': column, 'state': True} for column in columns]


def flatten_dictionnaries(columns: dict[str, str]):
    """Create list of True/False items using a list
    of columns that are dictionnaries"""
    data = []
    for column in columns:
        data.append(column['name'])
    return create_true_false_dictionnaries(data)
