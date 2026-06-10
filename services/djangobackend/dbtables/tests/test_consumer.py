from dbtables.tests.mixins import ConsumerMixin
from dbtables.utils import TableWebSocketActions

class TestTableCreationConsumer(ConsumerMixin):
    async def test_websocket_connection(self):
        connection = await self.create_connection()
        data = await connection.receive_json_from(timeout=5)
        self.assertEqual(data['action'], 'success')

        await connection.send_json_to({
            'action': TableWebSocketActions.CHECKOUT_FILE.value,
            'file': None
        })

        await connection.disconnect()
