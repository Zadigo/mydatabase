from faker import Faker
from factory.django import DjangoModelFactory
from endpoints.models import PublicApiEndpoint
from dbschemas.tests.utils import DatabaseSchemaFactory
from factory.declarations import SubFactory

faker = Faker()

class PublicApiEndpointFactory(DjangoModelFactory):
    class Meta:
        model = PublicApiEndpoint

    endpoint_uuid = faker.uuid4()
    endpoint = faker.name()
    
