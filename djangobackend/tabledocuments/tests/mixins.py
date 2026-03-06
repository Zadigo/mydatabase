from channels.testing import WebsocketCommunicator
from django.test import TestCase
from django.urls import re_path
from tabledocuments import consumers

from djangobackend.asgi import URLRouter


class ConsumerMixin(TestCase):
    def setUp(self):
        self.app = URLRouter([
            re_path(
                r'^ws/documents$',
                consumers.DocumentEditionConsumer.as_asgi()
            )
        ])

    async def create_connection(self):
        instance = WebsocketCommunicator(
            self.app,
            'ws/documents'
        )
        state, _ = await instance.connect()

        self.assertTrue(state)
        return instance

    async def test_connection(self):
        instance = await self.create_connection()
        await instance.disconnect()

        instance = await self.create_connection()
        await instance.disconnect()
        await instance.disconnect()
