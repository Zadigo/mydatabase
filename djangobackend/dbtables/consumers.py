from djangobackend.consumer_mixins import BaseConsumerMixin
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from dbtables.utils import ValidateWebsocketMessage
from dbtables.models import DatabaseTable

class TableCreationConsumer(BaseConsumerMixin, AsyncJsonWebsocketConsumer):
    """WebSocket consumer used on the table creation page in order
    to manage quick data manipulation and transactions on
    the table being created before it's actually saved in the database.
    """

    async def connect(self):
        await self.accept()

        table_id = self.scope['url_route']['kwargs']['table_id']
        await self.channel_layer.group_add(table_id, self.channel_name)
        await self.send_success('WebSocket connection established successfully')

    async def receive_json(self, content, **kwargs):
        # Here you would handle incoming messages from the client,
        # such as adding a new column, updating a cell value, etc.
        validated_data = ValidateWebsocketMessage(**content)

        table_id = self.scope['url_route']['kwargs']['table_id']
        try:
            table = await DatabaseTable.objects.aget(id=table_id)
        except DatabaseTable.DoesNotExist:
            await self.send_error('Table not found')
            return

    async def disconnect(self, close_code):
        # Handle any cleanup when the WebSocket connection is closed if necessary
        table_id = self.scope['url_route']['kwargs']['table_id']
        await self.channel_layer.group_discard(table_id, self.channel_name)
