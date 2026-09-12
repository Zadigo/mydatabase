import dataclasses
from typing import Any

from channels.generic.websocket import AsyncJsonWebsocketConsumer

from djangobackend.consumer_mixins import BaseConsumerMixin
from tabledocuments.logic.edit import DocumentEdition, DocumentTransform
from tabledocuments.utils import WebsocketActions
from tabledocuments.validation_models import (
    LoadedViaIdColumns,
    WsMessageModel,
    WsSendMessageModel,
)


# TODO: Rename to TableEditionConsumer
class DocumentEditionConsumer(BaseConsumerMixin, AsyncJsonWebsocketConsumer):
    """WebSocket consumer used on the editor side in order
    to manage quick data manipulation and transactions on
    the Google/Excel/CSV sheets"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.document_edition = DocumentEdition(self)
        self.document_transform = DocumentTransform(self.document_edition)
        self.database_id: int | None = None

    async def connect(self):
        await self.accept()
        await self.send_json({'action': 'connected'})

        self.database_id = self.scope['url_route']['kwargs']['database_id']

        if self.channel_layer is not None:
            await self.channel_layer.group_add(f'database_{self.database_id}', self.channel_name)

    async def disconnect(self, close_code):
        await self.close(code=close_code)

        if self.channel_layer is not None:
            await self.channel_layer.group_discard(f'database_{self.database_id}', self.channel_name)

    async def receive_json(self, content: dict[str, Any], **kwargs):
        model = WsMessageModel(**content)

        
        if model.action == WebsocketActions.LOAD_VIA_ID.value:
            if model.document is None:
                await self.send_error("Document UUID is missing")
                return

            state, document = await self.document_edition.load_document_by_id(model.document.uuid)

            if document is not None and dataclasses.is_dataclass(document):
                await self.document_transform.prepare(document)
                response = WsSendMessageModel(
                    action=WebsocketActions.LOAD_VIA_ID.value,
                    document_data=self.document_transform.stringify,
                    columns=LoadedViaIdColumns(
                        names=self.document_edition.column_names,
                        options=self.document_edition.column_options,
                        types=self.document_edition.column_types,
                        type_options=self.document_edition.column_type_options

                    )
                )
                await self.send_json(response.model_dump())
            else:
                await self.send_error(
                    f"Could not load document: {','.join(self.document_edition.errors)}"
                )
        elif model.action == WebsocketActions.LOAD_DOCUMENT_DATA.value:
            if model.document_uuid is None:
                await self.send_error('No document uuid provided')
                return

            state, document = await self.document_edition.load_document_by_id(model.document_uuid)
            response = WsSendMessageModel(
                action=WebsocketActions.LOAD_VIA_ID.value,
               document_data=self.document_transform.stringify
            )
            await self.send_json(response.model_dump())
        else:
            await self.send_error(f'Unknown action: {model.action}')
