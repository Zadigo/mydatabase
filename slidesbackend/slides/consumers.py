from channels import AsyncWebsocketConsumer


class SlideConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        # You can add logic here to handle the connection, like joining a group

    async def disconnect(self, close_code):
        # Handle disconnection logic if needed
        pass

    async def receive(self, text_data):
        # Handle incoming messages from the WebSocket
        await self.send(text_data="Message received")
