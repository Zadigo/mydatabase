import dataclasses
import uuid
from typing import Any
from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, PropertyMock, patch

import pandas
import requests
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator
from django.core.files.base import ContentFile
from django.test import TransactionTestCase
from django.urls import re_path, reverse
from tabledocuments import consumers
from tabledocuments.logic.edit import DocumentEdition, load_document_by_url
from tabledocuments.models import TableDocument

from djangobackend.utils import UnittestAuthenticationMixin


class TestRequestUtils(IsolatedAsyncioTestCase):
    async def test_load_document_by_url(self):
        test_url = 'https://jsonplaceholder.typicode.com/todos'
        response, errors = await load_document_by_url(test_url)
        self.assertIsNotNone(response, f'Failed to get response: {response}')
        self.assertListEqual(errors, [])

    # async def test_load_document_by_url_invalid_endpoint_data(self):
    #     test_url = 'http://example' # endpoint returns HTML text
    #     response, errors = await load_document_by_url(test_url)

    #     self.assertIsNotNone(response)
    #     self.assertListNotEqual(errors, [])


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

    async def test_idle_connect(self):
        instance = await self.create_connection()

        await instance.send_json_to({'action': 'idle_connect'})
        response = await instance.receive_json_from()
        await self.check_response(response)
        self.assertEqual(response, {'action': 'connected'})

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

    async def test_checkout_url(self):
        with patch.object(requests, 'get') as mocked_get:
            instance = await self.create_connection()

            mocked_response = MagicMock()

            type(mocked_response).status_code = PropertyMock(return_value=200)

            headers = {'Content-Type': 'application/json'}
            type(mocked_response).headers = PropertyMock(return_value=headers)

            mocked_response.json.return_value = [
                {
                    'firstname': 'Kendall',
                    'lastname': 'Jenner',
                    'age': 31
                }
            ]

            mocked_get.return_value = mocked_response

            await instance.send_json_to({
                'action': 'checkout_url',
                'url': 'http://example.com/endpoint.json'
            })

            response = await instance.receive_json_from()
            await self.check_response(response)
            action = response['action']
            self.assertEqual(action, 'processing_url', response)

            response = await instance.receive_json_from()
            await self.check_response(response)
            action = response['action']
            self.assertEqual(action, 'checkedout_url', response)
            self.assertIn('columns', response)


class TestApiEndpoints(TransactionTestCase, UnittestAuthenticationMixin):
    fixtures = ['fixtures/databases']

    def setUp(self):
        self.document = TableDocument.objects.first()

    def test_get_document(self):
        path = reverse('documents:retrieve_update_destroy_document', args=[
                       self.document.document_uuid])
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200, response.content)
        self.assertIsInstance(response.json(), dict)

    def test_update_document(self):
        path = reverse('documents:retrieve_update_destroy_document', args=[
                       self.document.document_uuid])
        response = self.client.patch(
            path, data={'name': 'Updated Document Name'}, content_type='application/json')
        self.assertEqual(response.status_code, 200, response.content)
        self.assertIsInstance(response.json(), dict)
        print(response.json())

    def test_delete_document(self):
        path = reverse('documents:retrieve_update_destroy_document', args=[
                       self.document.document_uuid])
        response = self.client.delete(path)
        self.assertEqual(response.status_code, 204, response.content)
