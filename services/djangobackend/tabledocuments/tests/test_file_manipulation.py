from tabledocuments.logic.utils import create_column_options
from tabledocuments.utils.file_manipulation import create_dataframe


def test_create_dataframe():
    data = [
        {"name": "Alice", "age": 30},
        {"name": "Bob", "age": 25}
    ]
    options = create_column_options(['name', 'age'])
    df = create_dataframe(data, options)

    assert not df.empty
    assert list(df.columns) == ["name", "age"]
