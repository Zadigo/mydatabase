from dbtables.tests.mixins import ConsumerMixin

class TestTableCreationConsumer(ConsumerMixin):
    async def test_websocket_connection(self):
        connection = await self.create_connection()
        # await connection.receive_json_from()

        # await connection.disconnect()
