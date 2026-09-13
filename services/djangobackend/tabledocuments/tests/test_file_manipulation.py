import pandas

from tabledocuments.tests.utils import build_column_options
from tabledocuments.utils.file_manipulation import create_dataframe
from tabledocuments.validation_models import ColumnOptionsModel, ColumnTypes


def test_create_dataframe(json_data):
    options = build_column_options('name', 'age')
    df = create_dataframe(json_data, options)

    assert not df.empty
    assert list(df.columns) == ["name", "age"]


def test_create_dataframe_with_booleans(json_data):
    for item in json_data:
        item['is_active'] = True
    
    options = build_column_options(
        'name', 'age', 'is_active', 
        column_types={'is_active': 'Boolean'}
    )
    df = create_dataframe(json_data, options)

    assert not df.empty
    assert list(df.columns) == ["name", "age", "is_active"]


def test_create_dataframe_none_nullable_columns():
    column_options = build_column_options('firstname', 'lastname', nullable=['lastname'])

    data = [
        {
            'firstname': 'Lucie',
            'lastname': None
        }
    ]

    df = create_dataframe(data, column_options)
    assert df.firstname.count() == 1


def test_create_dataframe_unique_columns():
    column_options = build_column_options('firstname', 'lastname', unique=['firstname'])

    data = [
        {
            'firstname': 'Jane',
            'lastname': 'Galoup'
        }
    ]

    df = create_dataframe(data, column_options)
    assert df.firstname.count() == 1



def test_column_type_check():
    options = [
        ColumnOptionsModel(name='firstname', columnType=ColumnTypes.STRING.value),
        ColumnOptionsModel(name='is_tall', columnType=ColumnTypes.BOOLEAN.value),
        ColumnOptionsModel(name='age', columnType=ColumnTypes.NUMBER.value),
        ColumnOptionsModel(name='hobbies', columnType=ColumnTypes.ARRAY.value),
        ColumnOptionsModel(name='profile', columnType=ColumnTypes.DICT.value)
    ]

    data = [
        {
            'firstname': 'Jane',
            'is_tall': 'true',
            'age': '30',
            'hobbies': '["reading", "swimming"]',
            'profile': '{"city": "New York", "job": "Engineer"}'
        }
    ]

    df = create_dataframe(data, options)

    assert df.is_tall.dtype == bool
    assert df.age.dtype == 'int64'


def test_create_dataframe_column_rename_creation():
    column_options = build_column_options('firstname', 'lastname', new_names={'firstname': 'FIRSTNAME'})

    df = create_dataframe(column_options, column_options)
    assert isinstance(df, pandas.DataFrame)
    assert df['FIRSTNAME'] is not None


def test_create_dataframe_not_visible_columns():
    column_options = build_column_options('firstname', 'lastname', not_visible=['lastname'])

    data = [
        {
            'firstname': 'Jane',
            'lastname': 'Doe',
            'is_active': 'true',
            'meta': '{"age": 30, "city": "New York"}'
        }
    ]

    df = create_dataframe(data, column_options)
    assert list(df.columns) == ['firstname']
