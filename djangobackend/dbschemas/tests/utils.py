from faker import Faker
from factory.django import DjangoModelFactory
from dbschemas.models import DatabaseSchema

faker = Faker()



class DatabaseSchemaFactory(DjangoModelFactory):
    class Meta:
        model = DatabaseSchema

    name = faker.word()
    database_functions = {}
    database_triggers = {}
    document_relationships = {}
