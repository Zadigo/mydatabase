from django.test import TestCase
import pandas
from tabledocuments.utils import create_dataframe
from tabledocuments.tests.utils import build_column_options

class TestCreateDataframe(TestCase):
    def test_simple_creation(self):
        data = [
            {
                'firstname': 'Jane',
                'lastname': 'Doe'
            }
        ]

        column_options = build_column_options('firstname', 'lastname')

        df = create_dataframe(data, column_options)
        self.assertIsInstance(df, pandas.DataFrame)
