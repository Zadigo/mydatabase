import pandas
import pytest

from tabledocuments.tests.utils import build_column_options
from tabledocuments.utils.file_manipulation import create_dataframe
from tabledocuments.validation_models import ColumnTypeOptionsModel, ColumnTypes


@pytest.fixture
def column_options():
    return [
        {
            'firstname': 'Jane',
            'lastname': 'Doe',
            'is_active': 'true',
            'meta': '{"age": 30, "city": "New York"}'
        }
    ]


def test_simple_creation():
    column_options = build_column_options('firstname', 'lastname')

    df = create_dataframe(column_options, column_options)
    assert isinstance(df, pandas.DataFrame)


def test_column_rename_creation():
    column_options = build_column_options('firstname', 'lastname', new_names={'firstname': 'FIRSTNAME'})

    df = create_dataframe(column_options, column_options)
    assert isinstance(df, pandas.DataFrame)
    assert df['FIRSTNAME'] is not None


def test_none_nullable_columns():
    column_options = build_column_options('firstname', 'lastname', nullable=['lastname'])

    data = [
        {
            'firstname': 'Lucie',
            'lastname': None
        }
    ]

    df = create_dataframe(data, column_options)
    assert df.firstname.count() == 1

def test_unique_columns():
    column_options = build_column_options('firstname', 'lastname', unique=['firstname'])

    data = [
        {
            'firstname': 'Jane',
            'lastname': 'Galoup'
        }
    ]

    df = create_dataframe(data, column_options)
    assert df.firstname.count() == 1

def test_visible_columns():
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

def test_column_type_check():
    options = [
        ColumnTypeOptionsModel(name='firstname', columnType=ColumnTypes.STRING.value),
        ColumnTypeOptionsModel(name='is_tall', columnType=ColumnTypes.BOOLEAN.value),
        ColumnTypeOptionsModel(name='age', columnType=ColumnTypes.NUMBER.value),
        ColumnTypeOptionsModel(name='hobbies', columnType=ColumnTypes.ARRAY.value),
        ColumnTypeOptionsModel(name='profile', columnType=ColumnTypes.DICT.value)
    ]

    options = [option.model_dump() for option in options]

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
    print(df)
    assert df.is_tall.dtype == bool
    assert df.age.dtype == 'int64'


