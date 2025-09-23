import dataclasses
from typing import Any

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from tabledocuments.logic.edit import DocumentEdition, DocumentTransform
from tabledocuments.logic.utils import create_column_type_options, create_column_options
from djangobackend.consumer_mixins import BaseConsumerMixin


class DocumentEditionConsumer(BaseConsumerMixin, AsyncJsonWebsocketConsumer):
    """WebSocket consumer used on the editor side in order
    to manage quick data manipulation and transactions on
    the Google/Excel/CSV sheets"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.document_edition = DocumentEdition(self)
        self.document_transform = DocumentTransform()

    async def connect(self):
        await self.accept()

        # user = self.scope['user']
        # print(user)

        # if not user.is_authenticated:
        #     await self.close(code=1000)
        #     return

    async def disconnect(self, close_code):
        await self.close(code=close_code)

    async def receive_json(self, content: dict[str, Any], **kwargs):
        action = content['action']

        if action == 'idle_connect':
            await self.send_json({'action': 'connected'})
        elif action == 'load_via_id':
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
        elif action == 'checkout_url':
            document = await self.document_edition.load_json_document_by_url(content['url'])
            if document is not None:
                columns = document.content.columns.tolist()

                await self.send_json({
                    'action': 'checkedout_url',
                    'columns': {
                        'names': columns,
                        'options': create_column_options(columns),
                        'type_options': create_column_type_options(columns)
                    }
                })
        else:
            await self.send_error(f'Unknown action: {action}')
