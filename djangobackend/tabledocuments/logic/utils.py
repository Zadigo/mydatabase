def create_column_type_options(columns: list[str]):
    """Function that constrains the types of the column
    such uniqueness or nullity or the type of data it holds"""
    return list(
        map(
            lambda column: {
                'name': column,
                'newName': column,
                'columnType': 'String',
                'unique': False,
                'nullable': True
            },
            columns
        )
    )


def create_column_options(columns: list[str]):
    """Function that creates column options that is used
    in the frontend to toggle visibility, editability or
    other functionalities on specific given columns"""
    return list(
        map(
            lambda column: {
                'name': column,
                'visible': True,
                'editable': True,
                'sortable': True,
                'searchable': True
            },
            columns
        )
    )


def user_preference_column_options(columns: list[str]):
    """Function that creates column options that the user can
    set as preferences for the final table presentation. This is used
    when the user wants to save their preferences for a given document"""
    result = create_column_type_options(columns)
    return [x.update(visible=True) for x in result]


def clean_user_column_type_options(column_options: list[dict]):
    """Function that cleans the user column type options by removing
    any fields that are not expected. This is used when the user sends
    their preferences for a given document to the backend, to ensure that
    only valid fields are processed."""
    expected_fields = ['name', 'newName', 'columnType', 'unique', 'nullable']
    
    clean_options: list[dict] = []
    for option in column_options:
        clean_option = {}
        for field in expected_fields:
            clean_option[field] = option[field]
        clean_options.append(clean_option)
    return clean_options
