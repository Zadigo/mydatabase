import dataclasses
from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, PropertyMock, patch

import pandas
import requests
from channels.db import database_sync_to_async
from django.core.files.base import ContentFile

from tabledocuments.logic.edit import DocumentEdition
from tabledocuments.models import TableDocument


class TestDocumentEdition(IsolatedAsyncioTestCase):
    """Tests for the DocumentEdition class"""

    @classmethod
    def setUpClass(cls):
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
        self.test_url = 'http://example.com/endpoint.json'

    async def test_json_load_document_by_url_with_entry_key(self):
        with patch.object(requests, 'get') as mocked_get:
            instance = DocumentEdition()

            mocked_response = MagicMock()

            type(mocked_response).status_code = PropertyMock(return_value=200)
            type(mocked_response).headers = PropertyMock(
                return_value={'Content-Type': 'application/json'})
            mocked_response.json.return_value = self.fake_data

            mocked_get.return_value = mocked_response

            document = await instance.load_json_document_by_url(self.test_url)

            self.assertListEqual(
                instance.errors, [],
                "There were errors loading "
                f"the document: {', '.join(instance.errors)}"
            )

            self.assertIsNotNone(document)
            self.assertTrue(dataclasses.is_dataclass(document))
            self.assertIsInstance(document.document_cache_key, str)
            self.assertIsInstance(document.content, pandas.DataFrame)

            final_df = document.content
            self.assertEqual(final_df.shape[0], 2)

    async def test_fail_json_load_document_by_url(self):
        with patch.object(requests, 'get') as mocked_get:
            instance = DocumentEdition()

            mocked_response = MagicMock()

            type(mocked_response).status_code = PropertyMock(return_value=500)
            type(mocked_response).headers = PropertyMock(
                return_value={'Content-Type': 'application/json'})
            mocked_response.json.return_value = {
                'error': 'Internal Server Error'}

            mocked_get.return_value = mocked_response

            document = await instance.load_json_document_by_url(self.test_url)
            self.assertIsNone(document)
            self.assertIn('Failed to load document', ' '.join(
                instance.errors), instance.errors)

    async def test_clean(self):
        df = pandas.DataFrame(self.fake_data)

        instance = DocumentEdition()
        instance.columns = ['firstname', 'lastname']
        cleaned_document = await instance.clean(df)

        # Assertions
        self.assertIsNotNone(cleaned_document)
        self.assertIsInstance(cleaned_document.document_cache_key, str)
        self.assertIsInstance(cleaned_document.content, pandas.DataFrame)

        final_df = cleaned_document.content
        self.assertListEqual(final_df.columns.tolist(), instance.columns)

        def lowercase_trigger(column: str, df: pandas.DataFrame) -> pandas.DataFrame:
            return df.assign(**{column: df[column].str.lower()})

        instance.column_triggers = {'firstname': lowercase_trigger}
        cleaned_document = await instance.clean(df)

        for item in cleaned_document.content.itertuples():
            with self.subTest(item=item):
                if isinstance(item.firstname, str):
                    self.assertTrue(item.firstname.islower())

    async def test_load_document_by_id(self):
        instance = DocumentEdition()

        @database_sync_to_async
        def create_table_document():
            table_document = TableDocument.objects.create(name='Some name')
            table_document.file.save(
                'test.csv', ContentFile('col1,col2\nval1,val2'))
            return table_document.id

        document_id = await create_table_document()

        dcoument = await instance.load_document_by_id(document_id)
        self.assertIsNotNone(dcoument)
        self.assertTrue(dataclasses.is_dataclass(dcoument))

