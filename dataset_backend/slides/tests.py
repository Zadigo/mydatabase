import json

from django.test import TestCase, TransactionTestCase
from django.urls import reverse
from slides.models import Block, Slide


class TestSlideApi(TransactionTestCase):
    fixtures = ['fixtures/users', 'fixtures/slides', 'fixtures/blocks']

    @property
    def _first_slide(self):
        return Slide.objects.first()

    def test_list_slides(self):
        path = reverse('slides_api:list')
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        for item in response.json():
            with self.subTest(item=item):
                self.assertIn('blocks', item)

    def test_create_slide(self):
        path = reverse('slides_api:create')
        response = self.client.post(path, data={'name': "Kendall's Fashion"})

        self.assertEqual(response.status_code, 201)
        for item in response.json():
            with self.subTest(item=item):
                self.assertIn('blocks', item)

    def test_slide_details(self):
        path = reverse('slides_api:details', args=[self._first_slide.slide_id])
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertIn('blocks', response.json())

    def test_view_final_slide(self):
        pass

    def test_update_slide(self):
        path = reverse('slides_api:update', args=[self._first_slide.slide_id])
        data = json.dumps({'name': 'Taylor Songs', 'data_source_id': None})
        headers = {'content-type': 'application/json'}

        response = self.client.patch(path, data=data, headers=headers)
        data = response.json()
        self.assertEqual(response.status_code, 200, 'Request not valid')
        self.assertIn('name', data, 'Missing name in response')
        self.assertIn('slide_data_source', data,
                      'Missing data source in response')

    def test_get_block(self):
        slide = self._first_slide
        block = self._first_slide.blocks.first()
        path = reverse('slides_api:block', args=[
                       slide.slide_id, block.block_id])
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertIn('id', response.json())

    def test_create_block(self):
        slide = self._first_slide
        path = reverse('slides_api:create_block', args=[slide.slide_id,])
        data = {
            'name': 'Test name',
            'component': 'table-block',
            'record_creation_columns': [],
            'record_update_columns': [],
            'search_columns': [],
            # 'block_data_source': None,
            'conditions': [],
            'user_filters': [],
            'active': True
        }
        response = self.client.post(path, data=data)

        self.assertEqual(response.status_code, 201)
        self.assertIn('name', response.json())

    def test_delete_block(self):
        block = Block.objects.create(name='Test name', slide=self._first_slide)
        path = reverse('slides_api:delete_block', args=[
            self._first_slide.slide_id,
            block.block_id
        ])
        response = self.client.post(path)
        self.assertEqual(response.status_code, 201)

    def test_update_block(self):
        pass

    def test_update_block_column(self):
        pass

    def test_filter_slide_data(self):
        pass

    def test_search_slide_data(self):
        pass
