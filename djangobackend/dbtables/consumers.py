from djangobackend.consumer_mixins import BaseConsumerMixin
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from dbtables.utils import TableWebSocketActions

class TableCreationConsumer(BaseConsumerMixin, AsyncJsonWebsocketConsumer):
    """WebSocket consumer used on the table creation page in order
    to manage quick data manipulation and transactions on
    the table being created before it's actually saved in the database.
    """

    async def connect(self):
        await self.accept()

        # table_id = self.scope['url_route']['kwargs']['table_id']
        # await self.channel_layer.group_add(table_id, self.channel_name)

    async def receive_json(self, content, **kwargs):
        pass
        # Here you would handle incoming messages from the client,
        # such as adding a new column, updating a cell value, etc.
        # validated_data = ValidateWebsocketMessage(**content)

        # table_id = self.scope['url_route']['kwargs']['table_id']
        # try:
        #     table = await DatabaseTable.objects.aget(id=table_id)
        # except DatabaseTable.DoesNotExist:
        #     await self.send_error('Table not found')
        #     return
        
        # if validated_data.action == TableWebSocketActions.CHECKOUT_URL.value:
        #     document = await self.document_edition.load_json_document_by_url(content['url'])

        #     if document is not None:
        #         columns = document.content.columns.tolist()

        #         await self.send_json({
        #             'action': 'checkedout_url',
        #             'columns': {
        #                 'names': columns,
        #                 'options': create_column_options(columns),
        #                 'type_options': create_column_type_options(columns)
        #             }
        #         })
        #     else:
        #         await self.send_error(
        #             f"Could not load document from URL: {','.join(self.document_edition.errors)}"
        #         )

        if validated_data.action == TableWebSocketActions.CHECKOUT_FILE.value:
            # Handle file checkout logic here
            pass

    async def disconnect(self, close_code):
        pass
        # Handle any cleanup when the WebSocket connection is closed if necessary
        # table_id = self.scope['url_route']['kwargs']['table_id']
        # await self.channel_layer.group_discard(table_id, self.channel_name)
