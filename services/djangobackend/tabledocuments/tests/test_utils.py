from django.test import TestCase
import pandas
from tabledocuments.utils import create_dataframe
from tabledocuments.tests.utils import build_column_options
from tabledocuments.validation_models import ColumnOption, ColumnTypes

class TestCreateDataframe(TestCase):
    def setUp(self):
        self.data = [
            {
                'firstname': 'Jane',
                'lastname': 'Doe'
            }
        ]

    def test_simple_creation(self):
        column_options = build_column_options('firstname', 'lastname')

        df = create_dataframe(self.data, column_options)
        self.assertIsInstance(df, pandas.DataFrame)

    def test_column_rename_creation(self):
        column_options = build_column_options('firstname', 'lastname', new_names={'firstname': 'FIRSTNAME'})

        df = create_dataframe(self.data, column_options)
        self.assertIsInstance(df, pandas.DataFrame)
        self.assertIsNotNone(df['FIRSTNAME'])

    def test_none_nullable_columns(self):
        column_options = build_column_options('firstname', 'lastname', nullable=['lastname'])

        self.data.append(
            {
                'firstname': 'Lucie',
                'lastname': None
            }
        )

        df = create_dataframe(self.data, column_options)
        self.assertTrue(df.firstname.count(), 1)

    def test_unique_columns(self):
        column_options = build_column_options('firstname', 'lastname', unique=['firstname'])

        self.data.append(
            {
                'firstname': 'Jane',
                'lastname': 'Galoup'
            }
        )

        df = create_dataframe(self.data, column_options)
        self.assertTrue(df.firstname.count(), 1)

    def test_visible_columns(self):
        column_options = build_column_options('firstname', 'lastname', not_visible=['lastname'])

        df = create_dataframe(self.data, column_options)
        self.assertListEqual(list(df.columns), ['firstname'])

    def test_column_type_check(self):
        options = [
            ColumnOption(name='firstname', columnType=ColumnTypes.STRING.value),
            ColumnOption(name='is_tall', columnType=ColumnTypes.BOOLEAN.value),
            ColumnOption(name='age', columnType=ColumnTypes.NUMBER.value),
            ColumnOption(name='hobbies', columnType=ColumnTypes.ARRAY.value),
            ColumnOption(name='profile', columnType=ColumnTypes.DICT.value)
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
        # self.assertTrue(df.is_tall.dtype == bool)
        # self.assertTrue(df.age.dtype == 'int64')


