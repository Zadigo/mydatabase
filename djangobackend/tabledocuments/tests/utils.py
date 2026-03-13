from factory.django import DjangoModelFactory
from faker import Faker as FakerClass
from tabledocuments.models import TableDocument
from django.core.files.base import ContentFile

faker = FakerClass()


class DocumentFactory(DjangoModelFactory):
    class Meta:
        model = TableDocument

    name = faker.file_name(extension='csv')
    column_names = ['firstname', 'lastname']
    url = 'https://jsonplaceholder.typicode.com/users'


class FileBasedTableDocumentFactory(DjangoModelFactory):
    class Meta:
        model = TableDocument

    document_uuid = faker.uuid4()
    name = faker.word()
    file = None
    column_names = []
    column_options = {}
    column_types = {}
    url = None
    google_sheet_id = None


def create_file_based_instance() -> TableDocument:
    instance = FileBasedTableDocumentFactory.create()
    
    # Create a sample CSV file
    csv_content = "firstname,lastname\nJohn,Doe\nJane,Smith"    
    content_file = ContentFile(csv_content.encode('utf-8'), name=f"{instance.document_uuid}.csv")
    instance.file.save(f"{instance.document_uuid}.csv", content_file, save=True)

    return instance
