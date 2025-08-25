from channels.generic.websocket import AsyncJsonWebsocketConsumer
from tabledocuments.logic.edit import DocumentEdition
from django.core.files import File
from djangobackend.consumer_mixins import BaseConsumerMixin


class DatabaseConsumer(BaseConsumerMixin, AsyncJsonWebsocketConsumer):
    """WebSocket consumer used on the editor side in order
    to manage quick data manipulation and transactions on
    the Google/Excel/CSV sheets"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.document_edition = DocumentEdition()

    async def connect(self):
        await self.accept()

        user = self.scope['user']

        if not user.is_authenticated:
            await self.close(code=1000)
            return

    async def disconnect(self, close_code):
        await self.close(code=close_code)

    async def receive_json(self, content, **kwargs):
        action = content['action']

        if action == 'idle_connect':
            pass
        elif action  == 'load_url':
            document = await self.document_edition.load_document_by_url(content['url'], partial=True)
            if document is not None:
                await self.send_json({
                    'action': 'url_loaded',
                    'data': document.content.to_json(orient='records', force_ascii=False),
                    'document_id': document.document_id
                })

                # Create the document in the database
                file_instance = File(document.content.to_csv(index=False), document.document_id)
            else:
                await self.send_error(f'Failed to load document from URL: {content["url"]}')
        elif action == 'load_data':
            pass
        else:
            await self.send_error(f'Unknown action: {action}')
