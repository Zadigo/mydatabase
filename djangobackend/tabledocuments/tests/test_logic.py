import dataclasses
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock

import pandas
from asgiref.sync import async_to_sync
from django.core.files.base import ContentFile
from factory.django import DjangoModelFactory
from faker import Faker as FakerClass
from tabledocuments.logic.edit import (DocumentEdition, DocumentTransform,
                                       load_document_by_url)
from tabledocuments.models import TableDocument
from tabledocuments.tests.mixins import ConsumerMixin

faker = FakerClass()


class DocumentFactory(DjangoModelFactory):
    class Meta:
        model = TableDocument

    name = faker.file_name(extension='csv')
    column_names = ['firstname', 'lastname']
    url = 'https://jsonplaceholder.typicode.com/users'


class TestLogicDocumentEdition(ConsumerMixin):
    def setUp(self):
        super().setUp()

        consumer = AsyncMock()
        self.documents = DocumentFactory.create_batch(5)
        self.instance = DocumentEdition(consumer)

    def test_document_edition_instance(self):
        document = TableDocument.objects.first()
        data = async_to_sync(
            self.instance.load_json_document_by_url
        )(document.url)

        self.assertIsNotNone(data)

    def test_clean(self):
        instance = DocumentEdition()
        instance.columns = ['name']

        values = [
            {
                'name': faker.first_name(),
                'lastname': faker.last_name(),
                'age': faker.random_int(min=18, max=40)
            }
        ]

        df = pandas.DataFrame(values)

        # Test clean with no triggers + default column options
        doc = async_to_sync(instance.clean)(df)
        self.assertListEqual(list(doc.content.columns), ['name'])

        # Test column triggers
        instance.column_triggers = {
            'name': lambda col, df: df['name'].str.upper()
        }

        data = async_to_sync(instance.clean)(df)
        self.assertIsNotNone(data)

    def test_finalize(self):
        pass

    def test_load_document_by_id(self):
        document = TableDocument.objects.first()
        document.file.save(
            document.name,
            ContentFile(b'name\nJohn\n')
        )
        document.save()

        doc = async_to_sync(self.instance.load_document_by_id)(document.id)
        self.assertIsNotNone(doc)
        document.file.delete()

    def test_load_json_document_by_url(self):
        instance = DocumentEdition()
        doc = async_to_sync(instance.load_json_document_by_url)(
            'https://jsonplaceholder.typicode.com/users'
        )
        self.assertIsNotNone(doc)
        self.assertTrue(dataclasses.is_dataclass(doc))


class TestLogicDocumentTransform(ConsumerMixin):
    def setUp(self):
        super().setUp()

        consumer = AsyncMock()
        self.documents = DocumentFactory.create_batch(5)
        self.instance = DocumentTransform(consumer)

    async def test_load_document(self):
        aync_to_sync(self.instance.load_document)()


class TestLogicUtils(IsolatedAsyncioTestCase):
    async def test_load_document_by_url(self):
        data, errors = await load_document_by_url(
            'https://jsonplaceholder.typicode.com/'
        )
        self.assertEqual(errors, [])
        self.assertTrue(dataclasses.is_dataclass(data))
