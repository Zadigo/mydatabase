import pytest
from tabledocuments.utils import WebsocketActions
from tabledocuments.ws_models import DocumentInfoModel, WsMessageModel
from tabledocuments.


@pytest.mark.django_db
async def test_load_document_via_id(ws_documents):
    response = await ws_documents.receive_json_from()

    assert response is not None
    assert response['action'] == 'connected'

    model = WsMessageModel(
        action=WebsocketActions.LOAD_VIA_ID.value,
        table_id='1',
        document=DocumentInfoModel(
            uuid='something',
            name='Some table'
        )
    )
    await ws_documents.send_json_to(model.model_dump())

    response = await ws_documents.receive_json_from()

    assert response is not None
    assert response['action'] == 'loaded_via_id'

    await ws_documents.disconnect()
