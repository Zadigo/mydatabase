import dataclasses
import datetime
import re
from typing import Any, Callable, TypeAlias

import pandas
import pytz
import requests
from channels.db import database_sync_to_async
from django.core.cache import cache
from django.utils.crypto import get_random_string
from requests.models import Response
from tabledocuments.models import TableDocument

# endpoint test: https://data.opendatasoft.com/api/explore/v2.1/catalog/datasets/cfa@datailedefrance/records?limit=20

PostReadTrigger: TypeAlias = dict[
    str, 
    Callable[[
        str, pandas.DataFrame
    ], 
    pandas.DataFrame
]]


@dataclasses.dataclass
class Document:
    document_cache_key: str
    content: pandas.DataFrame
    metadata: dict[str, str | bool] = dataclasses.field(default_factory=dict)

    def __hash__(self):
        return hash((self.document_cache_key))


class DocumentEdition:
    """A classs that preloads and reads a document
    for edition in the frontend"""

    def __init__(self):
        self.errors: list[str] = []
        self.columns: list[str] = []

        # Triggers to run on the columns of the dataframe when the
        # read is complete (e.g. transform data operations etc.)
        self.column_triggers: PostReadTrigger = {}

    async def finalize(self, document_cache_key: str, df: pandas.DataFrame, metadata: dict[str, str | bool] = {}):
        metadata['date'] = str(datetime.datetime.now(tz=pytz.UTC))
        return Document(document_cache_key=document_cache_key, content=df, metadata=metadata)

    async def clean(self, df: pandas.DataFrame, metadata: dict[str, str | bool] = {}, **options: dict):
        # Before running document operations,
        # save it to the cache with a unique key
        document_cache_key = f"document_{get_random_string(length=10)}"

        # Some documents might have invalid characters in their
        # column title. Deal with this here.
        for column in df.columns:
            df = df.rename(columns={column: re.sub(r'[^\w\s]', '', column)})

        # Cache the whole document to prevent reading
        # the whole file all the time
        cache.set(document_cache_key + '-raw', df,
                  timeout=(24 * 60 * 60))  # 24 hour

        if self.columns:
            df = df[self.columns]

        if self.column_triggers:
            for column, trigger in self.column_triggers.items():
                df = trigger(column, df)
            cache.set(
                document_cache_key + '-transformed',
                df, timeout=(60 * 60)
            )  # 1 hour

        # Return only a partial view of the dataframe
        # to the frontend
        partial: bool = options.get('partial', True)
        partial_limit: int = options.get('partial_limit', 20)

        if partial:
            df = df.head(n=partial_limit)

        return await self.finalize(document_cache_key=document_cache_key, df=df, metadata=metadata)

    async def load_document_by_id(self, id: int | str) -> Document | bool:
        """Loads the data in a document using the database"""

        @database_sync_to_async
        def get_document() -> tuple[bool, pandas.DataFrame | None]:
            document = TableDocument.objects.get(id=id)

            if document.file is None:
                self.errors.append(
                    'The document does not have a file associated with it')
                return False, None

            try:
                # Some csv files contain ";" and Pandas will throw an
                # error if this separator is not explicity indicated since it
                # logically expects commas.
                # So try to load the document using the classic ","
                # separator if not got to ";"
                return True, pandas.read_csv(document.file.path)
            except:
                try:
                    return True, pandas.read_csv(document.file.path, sep=';')
                except:
                    # Accept *ONLY* "," or ";". If pandas cannot read the separator
                    # we are not going to waste time trying to guess or get it.
                    # The onus is on the user to ensure that the file is either
                    # comma or semicolon separated
                    self.errors.append(
                        "File does not contain a valid separator. "
                        "Accepted separators are: ',' or ';'"
                    )
                    return False, None
        is_valid, df = await get_document()

        if not is_valid:
            return False

        return await self.clean(df)

    async def load_document_by_url(self, url: str, **request_params: Any) -> Response | None:
        try:
            response = requests.get(url, headers={}, **request_params)
        except requests.RequestException as e:
            self.errors.append(str(e))
            return None
        else:
            return response

    async def load_json_document_by_url(self, url: str, entry_key: str | None = None, **request_params: Any) -> Document | None:
        """Function used to load the content of document returned via an API endpoint
        as a json format. The content will be loaded and transformed back to a csv database file.

        Since the the actual data in a JSON file is not always at the root, the entry key can be used 
        to specify the path to the data. For example: items in `{'items': []}` or root.items
        in `{'root': {'items': []}}`
        """
        response = await self.load_document_by_url(url, **request_params)
        if response is not None and response.ok:
            try:
                data = response.json()
            except ValueError:
                self.errors.append("Failed to parse JSON response")
                return None
            else:
                # Get the document type via the headers e.g application/csv
                content_type = response.headers.get('Content-Type', '')

                if 'application/json' not in content_type:
                    self.errors.append(
                        "Unhandled document type. Valid types are: json")
                    return None

                if entry_key is not None:
                    # Override the data with the entry key
                    # since we do not really care about the
                    # root structure
                    keys = entry_key.split('.')
                    for key in keys:
                        data = data.get(key, {})

                if isinstance(data, dict):
                    self.errors.append(
                        'Trying to build data from a dict? If this is not '
                        'intended, please provide an entry key'
                    )
                    return None

                try:
                    # By any means, if the data is not valid, pandas
                    # will also automatically raise an error
                    df = pandas.DataFrame(data)
                    print(df)
                except:
                    self.errors.append(
                        "Failed to create DataFrame from JSON data")
                else:
                    return await self.clean(df, {'url': url})
        return None


class DocumentTransform:
    """This is the main class that handles live document
    aka data transformation"""

    def __init__(self):
        self.current_document: Document | None = None
        self.initial_dataframe: pandas.DataFrame | None = None

        self.column_names: list[str] = []
        self.column_type_options: list[dict[str, str | bool ]] = []
        self.column_options: list[dict[str, str | bool]] = []
        # self.column_types: list[dict[str, str]] = []

    @property
    def can_transform(self):
        return self.current_document is not None

    @property
    def stringify(self) -> str:
        """Returns a string version of the data which can
        then be sent over websockets essentially"""
        if self.current_document is not None:
            return self.current_document.content.to_json(orient='records', force_ascii=False)
        return ''

    async def load_document(self, document: Document):
        self.current_document = document
        # Since the Document dataclass only contains the partial data
        # contained in the whole dataset, we need to load the original
        # dataset from memory
        cache_key = self.current_document.document_cache_key + '-raw'
        self.initial_dataframe = cache.get(cache_key, None)

        self.column_names = document.content.columns.tolist()

        # Column type options allows the user to modify the column
        # type and so as uniqueness and nullity
        self.column_type_options = list(
            map(
                lambda column: {
                    'name': column,
                    'columnType': 'String',
                    'unique': False,
                    'nullable': True
                },
                self.column_names
            )
        )

        # Column options allws the user to spcify which columns 
        # are editable, visible etc to the end user
        self.column_options = list(
            map(
                lambda column: {
                    'name': column,
                    'visible': True,
                    'editable': True,
                    'sortable': True,
                    'searchable': True
                },
                self.column_names
            )
        )

        # This builds the column types that will be
        # modified by the user. By default, every
        # column is considered as a string [String]
        # self.column_types = list(
        #     map(
        #         lambda column: {
        #             ''
        #         }
        #     )
        # )

    async def create_foreign_key(self, lh_document, rh_document, relationship_fields: list[str] = [], select: list[str] = []):
        """Artificially create a foreign key between two documents. The end
        user will then be able to view documents who are not merged as one

        * `lh_document`: The left-hand document
        * `rh_document`: The right-hand document
        * `relationship_fields`: The fields to use for the relationship
        * `select`: The fields to select from the documents
        """
        return NotImplemented

    async def merge_documents(self, *documents):
        """Merge multiple documents into one using the
        initial document as a base"""
        return NotImplemented

    async def transform_data_types(self, datatypes: dict[str, str]):
        """Enables the document owner to indicate what type of
        data types are present in the document"""
        accepted_data_types = [
            'String', 'Number', 'Boolean', 'Date',
            'Datetime', 'Array', 'Dict'
        ]
