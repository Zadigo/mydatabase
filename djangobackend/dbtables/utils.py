from pydantic import BaseModel


class ValidateWebsocketMessage(BaseModel):
    action: str
    payload: dict


class TableWebSocketActions:
    CHECKOUT_URL = 'checkout_url'
