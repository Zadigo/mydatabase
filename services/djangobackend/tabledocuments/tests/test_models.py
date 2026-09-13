import pytest

from tabledocuments.models import TableDocument
from tabledocuments.tests.utils import DocumentFactory, create_file_based_instance
from tabledocuments.validation_models import ColumnOptionsModel


@pytest.mark.django_db
def test_model_creation():
    instance = create_file_based_instance()
    assert instance.file is not None, instance.file
    instance.file.delete(save=True)


@pytest.mark.django_db
def test_mixed_options():
    instance: TableDocument = DocumentFactory.create()

    options = ColumnOptionsModel(name='firstname')
    instance.column_options = [options.model_dump()]
    
    instance.save()

    assert instance.column_options is not None
    assert instance.column_types is not None
