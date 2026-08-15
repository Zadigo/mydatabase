import enum

from pydantic import BaseModel


class ValidateWebsocketMessage(BaseModel):
    action: str
    file: bytes | None = None


class TableWebSocketActions(enum.Enum):
    CHECKOUT_URL = 'checkout_url'
    CHECKOUT_FILE = 'checkout_file'
