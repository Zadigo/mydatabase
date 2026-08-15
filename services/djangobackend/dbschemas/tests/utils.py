import json
import os
import pathlib

import factory
from django.conf import settings
from factory.django import DjangoModelFactory
from faker import Faker

from dbschemas.models import DatabaseProvider, DatabaseSchema

faker = Faker()


class DatabaseSchemaFactory(DjangoModelFactory):
    class Meta:
        model = DatabaseSchema

    name = faker.word()
    database_functions = {}
    database_triggers = {}
    document_relationships = {}


class DatabaseProviderFactory(DjangoModelFactory):
    class Meta:
        model = DatabaseProvider

    database_schema = factory.SubFactory(DatabaseSchemaFactory)
    google_sheet_api_key = None
    google_sheet_credentials = None


def add_provider_credentials(provider: DatabaseProvider, force_credentials: bool = False):
    api_key = os.environ.get('GOOGLE_SHEET_API_KEY', None)
    google_sheet_credentials = os.environ.get('GOOGLE_SHEET_CREDENTIALS', None)

    if force_credentials and (api_key is None or google_sheet_credentials is None):
        raise ValueError(
            "Environment variables GOOGLE_SHEET_API_KEY and GOOGLE_SHEET_CREDENTIALS must be set."
        )
    
    provider.google_sheet_api_key = api_key

    local_dir = pathlib.Path(settings.BASE_DIR).joinpath('credentials.json')

    path = pathlib.Path(google_sheet_credentials or local_dir)
    if path.exists():
        with path.open('r') as f:
            data = json.load(f)
            provider.google_sheet_credentials = data
            
    provider.save()


def create_provider_with_credentials(force_credentials: bool = False) -> DatabaseSchema:
    instance: DatabaseSchema = DatabaseSchemaFactory.create()
    provider: DatabaseProvider = instance.databaseprovider_set.get(database_schema=instance)
    add_provider_credentials(provider, force_credentials=force_credentials)
    return instance
