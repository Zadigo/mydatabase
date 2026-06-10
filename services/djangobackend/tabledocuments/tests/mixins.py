from channels.testing import WebsocketCommunicator
from unittest import IsolatedAsyncioTestCase
from django.urls import re_path
from tabledocuments import consumers
from djangobackend.asgi import URLRouter


class ConsumerMixin(IsolatedAsyncioTestCase):
    def setUp(self):
        self.app = URLRouter(
            [
                re_path(
                    r'^ws/documents$',
                    consumers.DocumentEditionConsumer.as_asgi(),
                )
            ]
        )

    async def create_connection(self):
        instance = WebsocketCommunicator(
            self.app,
            r'^ws/documents$'
        )
        state, _ = await instance.connect()

        self.assertTrue(state)
        return instance

    async def test_connection(self):
        instance = await self.create_connection()
        await instance.disconnect()
