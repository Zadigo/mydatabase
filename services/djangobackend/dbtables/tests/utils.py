from faker import Faker
from factory.django import DjangoModelFactory
from dbtables.models import DatabaseTable
from factory.declarations import SubFactory
from dbschemas.tests.utils import DatabaseSchemaFactory

faker = Faker()

class DatabaseTableFactory(DjangoModelFactory):
    class Meta:
        model = DatabaseTable

    name = faker.word()
    description = faker.text()
    database_schema = SubFactory(DatabaseSchemaFactory)
