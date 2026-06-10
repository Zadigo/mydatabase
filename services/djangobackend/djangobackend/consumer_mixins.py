
class BaseConsumerMixin:
    async def send_error(self, error_message: str):
        await self.send_json({
            'action': 'error',
            'message': error_message
        })

    async def send_success(self, success_message: str):
        await self.send_json({
            'action': 'success',
            'message': success_message
        })
