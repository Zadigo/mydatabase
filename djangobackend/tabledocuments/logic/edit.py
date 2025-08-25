import dataclasses
import re
from typing import Callable, TypeAlias

import pandas
import requests
from django.core.cache import cache
from django.utils.crypto import get_random_string

# endpoint test: https://data.opendatasoft.com/api/explore/v2.1/catalog/datasets/cfa@datailedefrance/records?limit=20

PostReadTrigger: TypeAlias = dict[str, Callable[[str, pandas.DataFrame], pandas.DataFrame]]


@dataclasses.dataclass
class Document:
    document_id: str
    content: pandas.DataFrame
    metadata: dict[str, str | bool] = dataclasses.field(default_factory=dict)

    def __hash__(self):
        return hash((self.document_id))


class DocumentEdition:
    """A classs that preloads and reads a document
    for edition in the frontend"""

    def __init__(self, **options: str | bool | list[str]):
        self.errors: list[str] = []
        self.columns: list[str] = []

        if isinstance(options.get('columns'), list):
            self.columns = options['columns']

        # Return only a partial view of the dataframe
        self.partial: bool = options.get('partial', False)
        self.partial_limit: int = options.get('partial_limit', 50)

        # Triggers to run on the columns of the dataframe when the
        # read is complete (e.g. transform data operations etc.)
        self.column_triggers: PostReadTrigger = options.get('post_read_triggers', {})

    async def finalize(self, document_id: str, df: pandas.DataFrame, metadata: dict[str, str | bool] = {}):
        return Document(document_id=document_id, content=df, metadata=metadata)

    async def clean(self, df: pandas.DataFrame, metadata: dict[str, str | bool] = {}):
        # Before running document operations,
        # save it to the cache with a unique key
        document_id = f"document_{get_random_string(length=10)}"

        # Some documents might have invalid characters in their
        # column title. Deal with this here.
        for column in df.columns:
            df = df.rename(columns={column: re.sub(r'[^\w\s]', '', column)})

        # Cache the whole document to prevent reading
        # the whole file all the time
        cache.set(document_id + '-raw', df, timeout=(24 * 60 * 60))  # 24 hour

        if self.columns:
            df = df[self.columns]

        if self.column_triggers:
            for column, trigger in self.column_triggers.items():
                df = trigger(column, df)
            cache.set(document_id + '-transformed', df, timeout=(60 * 60))  # 1 hour

        if self.partial:
            df = df.head(n=self.partial_limit)

        return await self.finalize(document_id=document_id, df=df)

    async def load_document_by_id(self, id: str) -> pandas.DataFrame:
        pass

    async def load_document_by_url(self, url: str, **params):
        """Loads a new document using an API endpoint"""
        try:
            response = requests.get(url, headers={}, **params)
        except requests.RequestException as e:
            self.errors.append(str(e))
            return None
        else:
            if response.ok:
                try:
                    data = response.json()
                except ValueError:
                    self.errors.append("Failed to parse JSON response")
                    return None
                else:
                    return await self.clean(pandas.DataFrame(data))
            return None


class DocumentTransform:
    pass
