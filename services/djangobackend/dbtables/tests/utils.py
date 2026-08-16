from typing import Any
from unittest import IsolatedAsyncioTestCase

import factory
from channels.testing import WebsocketCommunicator
from django.urls import re_path
from factory.declarations import SubFactory
from factory.django import DjangoModelFactory
from faker import Faker

from dbschemas.tests.utils import DatabaseSchemaFactory
from dbtables import consumers
from dbtables.models import DatabaseTable
from djangobackend.asgi import URLRouter

faker = Faker()


class DatabaseTableFactory(DjangoModelFactory):
    class Meta:
        model = DatabaseTable

    name = factory.LazyAttribute(lambda x: faker.word())
    description = factory.LazyAttribute(lambda x: faker.sentence())
    database_schema = SubFactory(DatabaseSchemaFactory)


def create_table_with_schema[T = Any](schema: T) -> DatabaseTable:
    return DatabaseTableFactory.create(database_schema=schema)


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
