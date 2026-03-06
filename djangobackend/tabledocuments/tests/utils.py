
from factory.django import DjangoModelFactory
from faker import Faker as FakerClass
from tabledocuments.models import TableDocument

faker = FakerClass()


class DocumentFactory(DjangoModelFactory):
    class Meta:
        model = TableDocument

    name = faker.file_name(extension='csv')
    column_names = ['firstname', 'lastname']
    url = 'https://jsonplaceholder.typicode.com/users'
