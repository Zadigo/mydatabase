import dataclasses
import enum

import pandas


@dataclasses.dataclass
class Document:
    document_cache_key: str
    content: pandas.DataFrame
    metadata: dict[str, str | bool] = dataclasses.field(default_factory=dict)

    def __hash__(self):
        return hash(self.document_cache_key)


class WebsocketActions(enum.Enum):
    LOAD_VIA_ID = 'load_via_id'
    CHECKOUT_URL = 'checkout_url'
    LOAD_DOCUMENT_DATA = 'load_document_data'
