from asgiref.sync import sync_to_async
from tabledocuments.tests.mixins import ConsumerMixin
from tabledocuments.tests.utils import DocumentFactory
from tabledocuments.utils import WebsocketActions


class TestDocumentEditionConsumer(ConsumerMixin):
    async def test_connection(self):
        document = await sync_to_async(DocumentFactory.create)()

        conn = await self.create_connection()
        response = await conn.receive_json_from()

        # Test no action
        await conn.send_json_to({})
        response = await conn.receive_json_from()
        self.assertIn('No action provided', response['message'])

        # Test load via ID
        await conn.send_json_to({
            'action': WebsocketActions.LOAD_VIA_ID.value,
            'document': {
                'id': document.id
            }
        })

        response = await conn.receive_json_from()

        print(response)

        # Checkout Url

        await conn.disconnect()
