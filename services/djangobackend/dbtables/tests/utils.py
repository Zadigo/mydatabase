from dbschemas.tests.utils import DatabaseSchemaFactory
from factory.declarations import SubFactory
from factory.django import DjangoModelFactory
from faker import Faker

from dbtables.models import DatabaseTable

faker = Faker()

class DatabaseTableFactory(DjangoModelFactory):
    class Meta:
        model = DatabaseTable

    name = faker.word()
    description = faker.text()
    database_schema = SubFactory(DatabaseSchemaFactory)
