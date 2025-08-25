from typing import Any
from unittest import IsolatedAsyncioTestCase

import pandas
from asgiref.sync import async_to_sync
from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator
from django.test import TransactionTestCase
from django.urls import re_path
from djangobackend.utils import UnittestAuthenticationMixin
from tabledocuments import consumers
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

    async def test_json_load_document_by_url(self):
        document = await self.instance.load_json_document_by_url(self.test_url)

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


class TestDocumentEditionConsumer(TransactionTestCase, UnittestAuthenticationMixin):
    fixtures = ['fixtures/users']

    def setUp(self):
        self.consumer = consumers.DocumentEditionConsumer()
        self.app = URLRouter(
            [
                re_path(r'ws/documents/$', self.consumer.as_asgi())
            ]
        )
        self.client.headers
        self.use_authentication = False
        self.token = self.authenticate()

    async def create_connection(self):
        # For authentication to work (since we are querying the database)
        # we need to call it in a synchronous context
        if self.use_authentication:
            instance = WebsocketCommunicator(
                self.app, f'ws/documents/?token={self.token}')
        else:
            instance = WebsocketCommunicator(self.app, 'ws/documents/')

        connected, _ = await instance.connect()
        self.assertTrue(connected)
        return instance

    async def check_response(self, response: dict[str, Any]):
        """Responses should always have action in them so that
        the frontend knows how to route/handle them"""
        self.assertIn('action', response)

        if 'data' in response:
            self.assertIsInstance(response['data'], str)

    async def test_idle_connect(self):
        instance = await self.create_connection()

        await instance.send_json_to({'action': 'idle_connect'})
        response = await instance.receive_json_from()
        await self.check_response(response)
        self.assertEqual(response, {'action': 'connected'})

    async def test_load_url(self):
        instance = await self.create_connection()

        test_url = 'https://data.opendatasoft.com/api/explore/v2.1/catalog/datasets/cfa@datailedefrance/records?limit=20'
        await instance.send_json_to({'action': 'load_url', 'url': test_url})
        response = await instance.receive_json_from()
        await self.check_response(response)

        self.assertIn('data', response)
        self.assertIsInstance(response['data'], str)
        await self.check_response(response)

    async def test_with_authentication(self):
        self.use_authentication = True
        instance = await self.create_connection()
        print(instance.scope)
