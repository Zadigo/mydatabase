import pytest
from asgiref.sync import sync_to_async

from djangobackend.huey_app import huey_task
from tabledocuments.tests.utils import create_file_based_instance
from tabledocuments.utils import WebsocketActions
from tabledocuments.validation_models import DocumentInfoModel, WsMessageModel

huey_task.immediate = True

@pytest.mark.django_db
async def test_load_document_via_id(ws_documents):
    instance = await sync_to_async(create_file_based_instance)()

    response = await ws_documents.receive_json_from()

    assert response is not None
    assert response['action'] == 'connected'

    model = WsMessageModel(
        action=WebsocketActions.LOAD_VIA_ID.value,
        table_id='1',
        document=DocumentInfoModel(
            uuid=str(instance.document_uuid),
            name=instance.name
        )
    )
    await ws_documents.send_json_to(model.model_dump())

    response = await ws_documents.receive_json_from()

    assert response is not None
    assert response['action'] == 'load_via_id'

    await ws_documents.disconnect()


# class TestDocumentEditionConsumer(TransactionTestCase, UnittestAuthenticationMixin):
#     fixtures = ('fixtures/users', 'fixtures/databases')

#     def setUp(self):
#         self.consumer = consumers.DocumentEditionConsumer()
#         self.app = URLRouter(
#             [
#                 re_path(r'ws/documents/$', self.consumer.as_asgi())
#             ]
#         )
#         self.client.headers
#         self.use_authentication = False
#         self.token = self.authenticate()

#     async def create_connection(self):
#         # For authentication to work (since we are querying the database)
#         # we need to call it in a synchronous context
#         if self.use_authentication:
#             instance = WebsocketCommunicator(
#                 self.app, f'ws/documents/?token={self.token}')
#         else:
#             instance = WebsocketCommunicator(self.app, 'ws/documents/')

#         connected, _ = await instance.connect()
#         self.assertTrue(connected)
#         return instance

#     async def check_response(self, response: dict[str, Any]):
#         """Responses should always have action in them so that
#         the frontend knows how to route/handle them"""
#         self.assertIn('action', response)

#     async def test_idle_connect(self):
#         instance = await self.create_connection()

#         await instance.send_json_to({'action': 'idle_connect'})
#         response = await instance.receive_json_from()
#         await self.check_response(response)
#         self.assertEqual(response, {'action': 'connected'})

#     async def test_load_document_by_id(self):
#         instance = await self.create_connection()

#         @database_sync_to_async
#         def get_document():
#             document = TableDocument.objects.first()
#             if document is not None:
#                 # Create a fake csv file and save it on the
#                 # document, we will remove it later below
#                 document.file.save(
#                     'test.csv', ContentFile('col1,col2\nval1,val2'))
#                 return document.pk, document.name
#             return None, None

#         @database_sync_to_async
#         def remove_document_file(document_id: int):
#             document = TableDocument.objects.get(id=document_id)
#             document.file.delete()

#         pk, name = await get_document()

#         if pk is not None and name is not None:
#             await instance.send_json_to({
#                 'action': 'load_via_id',
#                 'document': {
#                     'id': pk,
#                     'name': name
#                 }
#             })

#             response = await instance.receive_json_from()
#             await self.check_response(response)

#             await remove_document_file(pk)

#     async def test_checkout_url(self):
#         with patch.object(requests, 'get') as mocked_get:
#             instance = await self.create_connection()

#             mocked_response = MagicMock()

#             type(mocked_response).status_code = PropertyMock(return_value=200)

#             headers = {'Content-Type': 'application/json'}
#             type(mocked_response).headers = PropertyMock(return_value=headers)

#             mocked_response.json.return_value = [
#                 {
#                     'firstname': 'Kendall',
#                     'lastname': 'Jenner',
#                     'age': 31
#                 }
#             ]

#             mocked_get.return_value = mocked_response

#             await instance.send_json_to({
#                 'action': 'checkout_url',
#                 'url': 'http://example.com/endpoint.json'
#             })

#             response = await instance.receive_json_from()
#             await self.check_response(response)
#             action = response['action']
#             self.assertEqual(action, 'processing_url', response)

#             response = await instance.receive_json_from()
#             await self.check_response(response)
#             action = response['action']
#             self.assertEqual(action, 'checkedout_url', response)
#             self.assertIn('columns', response)

