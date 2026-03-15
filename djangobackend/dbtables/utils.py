from typing import Optional

from pydantic import BaseModel
import enum

class ValidateWebsocketMessage(BaseModel):
    action: str
    file: Optional[bytes] = None


class TableWebSocketActions(enum.Enum):
    CHECKOUT_URL = 'checkout_url'
    CHECKOUT_FILE = 'checkout_file'
