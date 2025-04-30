from django.urls import re_path

from slides.api import views

app_name = 'slides_api'

urlpatterns = [
    re_path(
        r'^(?P<slide_id>sl\_[a-zA-Z0-9\-]+)/blocks/(?P<block_id>bl\_[a-zA-Z0-9\-]+)/search$',
        views.search_slide_data,
        name='search_slide_data'
    ),
    re_path(
        r'^(?P<slide_id>sl\_[a-zA-Z0-9\-]+)/blocks/(?P<block_id>bl\_[a-zA-Z0-9\-]+)/filter$',
        views.filter_slide_data,
        name='filter_slide_data'
    ),
    re_path(
        r'^(?P<slide_id>sl\_[a-zA-Z0-9\-]+)/blocks/(?P<block_id>bl\_[a-zA-Z0-9\-]+)/column/update$',
        views.update_block_column,
        name='update_block_column'
    ),
    re_path(
        r'^(?P<slide_id>sl\_[a-zA-Z0-9\-]+)/blocks/(?P<block_id>bl\_[a-zA-Z0-9\-]+)/update$',
        views.update_block,
        name='update_block'
    ),
    re_path(
        r'^(?P<slide_id>sl\_[a-zA-Z0-9\-]+)/blocks/(?P<block_id>bl\_[a-zA-Z0-9\-]+)/delete$',
        views.delete_block,
        name='delete_block'
    ),
    re_path(
        r'^(?P<slide_id>sl\_[a-zA-Z0-9\-]+)/blocks/(?P<block_id>bl\_[a-zA-Z0-9\-]+)$',
        views.get_block,
        name='block'
    ),
    re_path(
        r'^(?P<slide_id>sl\_[a-zA-Z0-9\-]+)/blocks/create$',
        views.create_block,
        name='create_block'
    ),
    re_path(
        r'^(?P<slide_id>sl\_[a-zA-Z0-9\-]+)/update$',
        views.update_slide,
        name='update'
    ),
    re_path(
        r'^(?P<slide_id>sl\_[a-zA-Z0-9\-]+)/final$',
        views.view_final_slide,
        name='final_slide'
    ),
    re_path(
        r'^(?P<slide_id>sl\_[a-zA-Z0-9\-]+)$',
        views.slide_details,
        name='details'
    ),
    re_path(
        r'^create$',
        views.create_slide,
        name='create'
    ),
    re_path(
        r'^$',
        views.list_slides,
        name='list'
    )
]
