from channels.testing import WebsocketCommunicator
from unittest import IsolatedAsyncioTestCase
from django.urls import re_path
from dbtables import consumers
from djangobackend.asgi import URLRouter


class ConsumerMixin(IsolatedAsyncioTestCase):
    def setUp(self):
        self.app = URLRouter(
            [
                re_path(
                    r'^ws/tables/(?P<table_id>\d+)$',
                    consumers.TableCreationConsumer.as_asgi(),
                )
            ]
        )

    async def create_connection(self):
        instance = WebsocketCommunicator(
            self.app,
            'ws/tables/1'
        )
        state, _ = await instance.connect()

        self.assertTrue(state)
        return instance

    async def test_connection(self):
        instance = await self.create_connection()
        await instance.disconnect()
