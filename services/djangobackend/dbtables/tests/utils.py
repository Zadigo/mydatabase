from typing import Any

import factory
from factory.declarations import SubFactory
from factory.django import DjangoModelFactory
from faker import Faker

from dbschemas.models import DatabaseSchema
from dbschemas.tests.utils import DatabaseSchemaFactory
from dbtables.models import DatabaseTable

faker = Faker()

class DatabaseTableFactory(DjangoModelFactory):
    class Meta:
        model = DatabaseTable

    name = factory.LazyAttribute(lambda x: faker.word())
    description = factory.LazyAttribute(lambda x: faker.sentence())
    database_schema = SubFactory(DatabaseSchemaFactory)


def create_table_with_schema[T = Any](schema: T) -> DatabaseTable:
    return DatabaseTableFactory.create(database_schema=schema)
