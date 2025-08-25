from typing import Awaitable, Callable, Coroutine, List, Type
from typing_extensions import Doc

import pandas
import dataclasses
import requests
from django.utils.crypto import get_random_string
from django.conf import settings
from django.core.cache import cache

# endpoint test: https://data.opendatasoft.com/api/explore/v2.1/catalog/datasets/cfa@datailedefrance/records?limit=20


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
        self.columns: list[str] = []

        if isinstance(options.get('columns'), list):
            self.columns = options['columns']

        # Return only a partial view of the dataframe
        self.partial: bool = options.get('partial', False)
        self.partial_limit: int = options.get('partial_limit', 50)

        # Triggers to run on the dataframe when the
        # read is complete (e.g. transform data operations etc.)
        self.post_read_triggers: List[Callable[[pandas.DataFrame], pandas.DataFrame]] = []

    async def finalize(self, document_id: str, df: pandas.DataFrame, metadata: dict[str, str | bool] = {}):
        return Document(document_id=document_id, content=df, metadata=metadata)

    async def clean(self, df: pandas.DataFrame, metadata: dict[str, str | bool] = {}):
        # Before running document operations,
        # save it to the cache with a unique key
        document_id = f"document_{get_random_string(length=10)}"
        cache.set(document_id, df, timeout=300)

        if self.post_read_triggers:
            for trigger in self.post_read_triggers:
                df = df.pipe(trigger)

        if self.columns:
            df = df[self.columns]

        if self.partial:
            df = df.head(n=self.partial_limit)

        return await self.finalize(document_id=document_id, df=df)

    async def load_document_by_id(self, id: str) -> pandas.DataFrame:
        return pandas.DataFrame()

    async def load_document_by_url(self, url: str, **params):
        """Loads a new document using an API endpoint"""
        try:
            response = requests.get(url, headers={}, **params)
        except requests.RequestException as e:
            return None
        else:
            if response.ok:
                return await self.clean(pandas.DataFrame(response.json()))
            return None


class DocumentTransform:
    pass
