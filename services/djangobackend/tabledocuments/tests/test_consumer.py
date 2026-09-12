import pytest
from asgiref.sync import sync_to_async

from djangobackend.huey_app import huey_task
from tabledocuments.tests.utils import create_file_based_instance
from tabledocuments.utils import WebsocketActions
from tabledocuments.ws_models import DocumentInfoModel, WsMessageModel

huey_task.immediate = True

@pytest.mark.django_db
async def test_load_document_via_id(ws_documents):
    instance = await sync_to_async(create_file_based_instance)()

    response = await ws_documents.receive_json_from()

    assert response is not None
    assert response['action'] == 'connected'

    model = WsMessageModel(
        action=WebsocketActions.LOAD_VIA_ID.value,
        table_id='1',
        document=DocumentInfoModel(
            uuid=str(instance.document_uuid),
            name=instance.name
        )
    )
    await ws_documents.send_json_to(model.model_dump())

    response = await ws_documents.receive_json_from()

    assert response is not None
    assert response['action'] == 'load_via_id'

    await ws_documents.disconnect()
