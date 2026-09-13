# class TestCheckoutDocument(TransactionTestCase):
#     # fixtures = ['fixtures/databases']
    
#     def setUp(self):
#         self.table: DatabaseTable = DatabaseTableFactory.create()

#         file_content = b'name,age\nAlice,30\nBob,25'
#         self.content_file = ContentFile(file_content, name='test.csv')

#     def test_checkout_file(self):
#         path = reverse('database_tables:checkout_document', args=[self.table.pk])
#         response = self.client.post(path, data={'file': self.content_file})
#         self.assertEqual(response.status_code, 200, response.content)
#         self.assertIn('sample', response.json())
#         self.assertIn('columns', response.json())
