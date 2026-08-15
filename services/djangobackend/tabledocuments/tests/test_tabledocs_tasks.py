import uuid

import pytest

from tabledocuments import django_tasks
from tabledocuments.models import TableDocument
from tabledocuments.tests.utils import (
    DocumentFactory,
    build_column_options,
    create_file_based_instance,
)
from tabledocuments.validation_models import ColumnOption


@pytest.fixture
def db():
    return create_file_based_instance()


@pytest.mark.django_db
class TestUpdateDocumentOptions:
    @classmethod
    def setup_class(cls):
        django_tasks.huey_task.immediate = True

    def test_with_no_params(self, db):
        django_tasks.update_document_options(db.document_uuid)
        assert db.column_options == []
        assert db.column_names == []

    def test_with_none_existing_database(self, db):
        pytest.skip(reason="Does not raise an exception")
        with pytest.raises(TableDocument.DoesNotExist):
            django_tasks.update_document_options(str(uuid.uuid4()))

    def test_with_from_file_param(self, db):
        django_tasks.update_document_options(db.document_uuid, from_file=True)
        expected_column_options = [
            {
                'name': 'firstname', 
                'newName': 'firstname', 
                'columnType': 'String', 
                'unique': False, 
                'nullable': True
            },
            {
                'name': 'lastname', 
                'newName': 'lastname', 
                'columnType': 'String', 
                'unique': False, 
                'nullable': True
            }
        ]
        db.refresh_from_db()
        assert db.column_type_options == expected_column_options

    def test_with_column_type_options_param(self, db):
        options = [
            ColumnOption(
                name='name',
                visible=True,
                editable=True,
                sortable=True,
                searchable=True
            )
        ]
        column_options = [item.model_dump() for item in options]
        django_tasks.update_document_options(db.document_uuid, column_type_options=column_options)

        db.refresh_from_db()
        assert db.column_type_options == []


@pytest.mark.django_db
class TestCreateFromCsvFile:
    @classmethod
    def setup_class(cls):
        django_tasks.huey_task.immediate = True

    @pytest.mark.django_db
    @pytest.mark.parametrize("data", [None, '', b''])
    def test_create_with_different_value_types(self, data):
        instance: TableDocument = DocumentFactory.create()

        django_tasks.create_csv_file_from_data(
            data=data,
            document_id=instance.id,
            column_type_options=[]
        )

    @pytest.mark.django_db
    def test_create_from_bytes(self):
        instance: TableDocument = DocumentFactory.create()
        
        django_tasks.create_csv_file_from_data(
            data= b'firstname,lastname\nJane,Doe',
            document_id=instance.id,
            column_type_options= build_column_options('firstname', 'lastname')
        )

        instance.refresh_from_db()
        assert instance.file is not None

    @pytest.mark.django_db
    def test_creation_with_semicolon(self):
        instance: TableDocument = DocumentFactory.create()

        django_tasks.create_csv_file_from_data(
            data= b'firstname;lastname\nJane;Doe',
            document_id=instance.id,
            column_type_options= build_column_options('firstname', 'lastname')
        )

        instance.refresh_from_db()
        assert instance.file is not None

    @pytest.mark.django_db
    def test_create_from_string(self):
        instance: TableDocument = DocumentFactory.create()

        django_tasks.create_csv_file_from_data(
            data='firstname,lastname\nJane,Doe',
            document_id=instance.id,
            column_type_options=build_column_options('firstname', 'lastname')
        )

        instance.refresh_from_db()
        assert instance.file is not None
