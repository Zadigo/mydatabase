from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

import pandas
from django.core.cache import cache
from django.test import TestCase
from tabledocuments.logic.edit import DocumentEdition


class TestDocumentEdition(IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fake_data = [
            {
                'firstname': 'Kendall',
                'lastname': 'Jenner',
                'age': 31
            },
            {
                'firstname': 'Kylie',
                'lastname': 'Jenner',
                'age': 24
            }
        ]

    def setUp(self):
        self.instance = DocumentEdition()
        self.test_url = 'https://data.opendatasoft.com/api/explore/v2.1/catalog/datasets/cfa@datailedefrance/records?limit=20'

    async def test_load_document_by_url(self):
        document = await self.instance.load_document_by_url(self.test_url)

        # Assertions
        self.assertIsNotNone(document)
        self.assertIsInstance(document.document_id, str)
        self.assertIsInstance(document.content, pandas.DataFrame)

        final_df = document.content
        self.assertEqual(final_df.shape[0], 20)

    async def test_clean(self):
        df = pandas.DataFrame(self.fake_data)

        self.instance.columns = ['firstname', 'lastname']
        cleaned_document = await self.instance.clean(df)

        # Assertions
        self.assertIsNotNone(cleaned_document)
        self.assertIsInstance(cleaned_document.document_id, str)
        self.assertIsInstance(cleaned_document.content, pandas.DataFrame)

        final_df = cleaned_document.content
        self.assertListEqual(final_df.columns.tolist(), self.instance.columns)

        def lowercase_trigger(column: str, df: pandas.DataFrame) -> pandas.DataFrame:
            return df.assign(**{column: df[column].str.lower()})

        self.instance.column_triggers = {'firstname': lowercase_trigger}
        cleaned_document = await self.instance.clean(df)

        for item in cleaned_document.content.itertuples():
            with self.subTest(item=item):
                if isinstance(item.firstname, str):
                    self.assertTrue(item.firstname.islower())
