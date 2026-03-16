import dataclasses
from typing import Any, Optional
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from tabledocuments.logic.edit import DocumentEdition, DocumentTransform
from tabledocuments.utils import WebsocketActions

from djangobackend.consumer_mixins import BaseConsumerMixin

# TODO: Rename to TableEditionConsumer
class DocumentEditionConsumer(BaseConsumerMixin, AsyncJsonWebsocketConsumer):
    """WebSocket consumer used on the editor side in order
    to manage quick data manipulation and transactions on
    the Google/Excel/CSV sheets"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.document_edition = DocumentEdition(self)
        self.document_transform = DocumentTransform()
        self.database_id: Optional[int] = None

    async def connect(self):
        await self.accept()
        await self.send_json({'action': 'connected'})

        self.database_id = self.scope['url_route']['kwargs']['database_id']
        await self.channel_layer.group_add(f'database_{self.database_id}', self.channel_name)

    async def disconnect(self, close_code):
        await self.close(code=close_code)
        await self.channel_layer.group_discard(f'database_{self.database_id}', self.channel_name)

    async def receive_json(self, content: dict[str, Any], **kwargs):
        try:
            action = content['action']
        except KeyError:
            await self.send_error('No action provided')
            return

        if action == WebsocketActions.LOAD_VIA_ID.value:
            document = content['document']
            document = await self.document_edition.load_document_by_id(document['id'])

            if document and dataclasses.is_dataclass(document):
                await self.document_transform.load_document(document)
                await self.send_json({
                    'action': 'loaded_via_id',
                    'document_data': self.document_transform.stringify,
                    'columns': {
                        'names': self.document_transform.column_names,
                        'options': self.document_transform.column_options,
                        'type_options': self.document_transform.column_type_options
                    }
                })
            else:
                await self.send_error(
                    f"Could not load document: {','.join(self.document_edition.errors)}"
                )
        else:
            await self.send_error(f'Unknown action: {action}')
