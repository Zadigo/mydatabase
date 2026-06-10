from channels.testing import WebsocketCommunicator
from unittest import IsolatedAsyncioTestCase
from django.urls import re_path
from dbtables import consumers
from djangobackend.asgi import URLRouter
from dbtables.models import DatabaseTable
from dbtables.tests.utils import DatabaseTableFactory


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
        self.table: DatabaseTable = DatabaseTableFactory.create()

    async def create_connection(self):
        instance = WebsocketCommunicator(
            self.app,
            f'ws/tables/{self.table.pk}'
        )
        state, _ = await instance.connect()

        self.assertTrue(state)
        return instance

    async def test_connection(self):
        instance = await self.create_connection()
        await instance.disconnect()
