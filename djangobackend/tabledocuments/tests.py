from typing import Any
from unittest import IsolatedAsyncioTestCase

import pandas
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator
from django.core.files.base import ContentFile
from django.test import TransactionTestCase
from django.urls import re_path
from tabledocuments import consumers
from tabledocuments.logic.edit import DocumentEdition
from tabledocuments.models import TableDocument

from djangobackend.utils import UnittestAuthenticationMixin


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
        self.test_url = 'https://data.opendatasoft.com/api/explore/v2.1/catalog/datasets/cfa@datailedefrance/records?limit=2'

    async def test_json_load_document_by_url_with_entry_key(self):
        document = await self.instance.load_json_document_by_url(self.test_url, entry_key='results')

        self.assertListEqual(
            self.instance.errors, [],
            f"There were errors loading the document: {', '.join(self.instance.errors)}"
        )

        # Assertions
        self.assertIsNotNone(document)
        self.assertIsInstance(document.document_id, str)
        self.assertIsInstance(document.content, pandas.DataFrame)

        final_df = document.content
        self.assertEqual(final_df.shape[0], 2)

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
    fixtures = ['fixtures/users', 'fixtures/databases']

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

        try:
            if 'document_data' in response:
                self.assertIsInstance(response['document_data'], str)
        except:
            print(response)

    async def test_idle_connect(self):
        instance = await self.create_connection()

        await instance.send_json_to({'action': 'idle_connect'})
        response = await instance.receive_json_from()
        await self.check_response(response)
        self.assertEqual(response, {'action': 'connected'})

    async def test_load_document_by_url(self):
        instance = await self.create_connection()

        test_url = 'https://data.opendatasoft.com/api/explore/v2.1/catalog/datasets/cfa@datailedefrance/records?limit=20'
        await instance.send_json_to({'action': 'load_via_url', 'url': test_url})
        response = await instance.receive_json_from()
        await self.check_response(response)

        self.assertIn('data', response)
        self.assertIsInstance(response['data'], str)
        await self.check_response(response)

    async def test_load_document_by_id(self):
        instance = await self.create_connection()

        @database_sync_to_async
        def get_document():
            document = TableDocument.objects.first()
            if document is not None:
                # Create a fake csv file and save it on the
                # document, we will remove it later below
                document.file.save(
                    'test.csv', ContentFile('col1,col2\nval1,val2'))
                return document.pk, document.name
            return None, None

        @database_sync_to_async
        def remove_document_file(document_id: int):
            document = TableDocument.objects.get(id=document_id)
            document.file.delete()

        pk, name = await get_document()

        if pk is not None and name is not None:
            await instance.send_json_to({
                'action': 'load_via_id',
                'document': {
                    'id': pk,
                    'name': name
                }
            })

            response = await instance.receive_json_from()
            await self.check_response(response)

            await remove_document_file(pk)

    # async def test_with_authentication(self):
    #     self.use_authentication = True
    #     instance = await self.create_connection()
    #     print(instance.scope)
