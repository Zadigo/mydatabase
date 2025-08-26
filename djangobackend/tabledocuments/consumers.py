import json
from typing import Any

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.core.files import File
from tabledocuments.logic.edit import DocumentEdition
from tabledocuments.models import TableDocument

from djangobackend.consumer_mixins import BaseConsumerMixin


class DocumentEditionConsumer(BaseConsumerMixin, AsyncJsonWebsocketConsumer):
    """WebSocket consumer used on the editor side in order
    to manage quick data manipulation and transactions on
    the Google/Excel/CSV sheets"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.document_edition = DocumentEdition()

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
        elif action == 'load_via_url':
            document = await self.document_edition.load_json_document_by_url(content['url'])
            if document is not None:
                await self.send_json({
                    'action': 'url_loaded',
                    'data': document.content.to_json(orient='records', force_ascii=False),
                    'document_id': document.document_id
                })

                # The document is in "memory" and returned to the user
                # as is. We still need to create a database entry for it

                name = content['name']

                @database_sync_to_async
                def create_document():
                    file_instance = File(document.content.to_csv(index=False), name=name)
                    instance = TableDocument.objects.create(name=name, file=file_instance)

                await create_document()
            else:
                await self.send_error(f'Failed to load document from URL: {content["url"]}')
        elif action == 'load_via_id':
            document = content['document']
            document = await self.document_edition.load_document_by_id(document['id'])
            await self.send_json({
                'action': 'data_loaded',
                'data': document
            })
        else:
            await self.send_error(f'Unknown action: {action}')
