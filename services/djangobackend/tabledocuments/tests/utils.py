from factory.django import DjangoModelFactory
from faker import Faker as FakerClass
from tabledocuments.models import TableDocument
from django.core.files.base import ContentFile
from django.core.files.base import ContentFile
from tabledocuments.models import TableDocument
from tabledocuments.validation_models import ColumnOption

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


def build_column_options(
    *columns: str, 
    new_names: dict = {}, 
    not_visible: list[str] = [], 
    not_editable: list[str] = [], 
    not_sortable: list[str] = [], 
    not_searchable: list[str] = [], 
    nullable: list[str] = [],
    unique: list[str] = [],
    **kwargs: bool
):
    """Returns a dictionnary of mixed options"""
    default_options = {
        'visible': True,
        'editable': True,
        'sortable': True,
        'searchable': True,
        'nullable': True,
        'unique': False
    }

    default_options = default_options | kwargs

    options = []
    for column in columns:

        instance = ColumnOption(
            name=column,
            **default_options
        )

        instance.visible = column not in not_visible 
        instance.editable = column not in not_editable
        instance.sortable = column in not_sortable 
        instance.searchable = column in not_searchable
        instance.nullable = False if column in nullable else True
        instance.unique = column in unique

        if column in new_names:
            instance.newName = new_names.get(column, None)

        options.append(instance.model_dump())
    return options
