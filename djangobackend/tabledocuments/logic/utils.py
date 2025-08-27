def create_column_type_options(columns: list[str]):
    """Function that creates column  types that can be used
    in the frontend to implement constraints"""
    return list(
        map(
            lambda column: {
                'name': column,
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
    other functionalities"""
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
