from unittest import IsolatedAsyncioTestCase

from channels.testing import WebsocketCommunicator

from dbtables import routing as table_routing
from djangobackend.asgi import URLRouter
from tabledocuments import routing as document_routing


class ConsumerMixin(IsolatedAsyncioTestCase):
    websocket_path = None

    def setUp(self):
        self.app = URLRouter(document_routing.urlpatterns + table_routing.urlpatterns)

    async def create_connection(self):
        instance = WebsocketCommunicator(
            self.app,
            self.websocket_path
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
