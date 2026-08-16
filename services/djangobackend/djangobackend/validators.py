from pydantic import BaseModel


class ValidateWebsocketMessage(BaseModel):
    action: str
    file: bytes | None = None

