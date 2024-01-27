from django.urls import re_path

from slides.api import views

urlpatterns = [
    re_path(
        r'^(?P<slide_id>sl\_[a-zA-Z0-9\-]+)/blocks/(?P<block_id>bl\_[a-zA-Z0-9\-]+)/column/update$',
        views.update_block_column
    ),
    re_path(
        r'^(?P<slide_id>sl\_[a-zA-Z0-9\-]+)/blocks/(?P<block_id>bl\_[a-zA-Z0-9\-]+)/update$',
        views.update_block
    ),
    re_path(
        r'^(?P<slide_id>sl\_[a-zA-Z0-9\-]+)/blocks/(?P<block_id>bl\_[a-zA-Z0-9\-]+)/delete$',
        views.delete_block
    ),
    re_path(
        r'^(?P<slide_id>sl\_[a-zA-Z0-9\-]+)/blocks/(?P<block_id>bl\_[a-zA-Z0-9\-]+)$',
        views.get_block
    ),
    re_path(
        r'^(?P<slide_id>sl\_[a-zA-Z0-9\-]+)/blocks/create$',
        views.create_block
    ),
    re_path(
        r'^(?P<slide_id>sl\_[a-zA-Z0-9\-]+)/update$',
        views.update_slide
    ),
    re_path(
        r'^(?P<slide_id>sl\_[a-zA-Z0-9\-]+)/final$',
        views.view_final_slide
    ),
    re_path(
        r'^(?P<slide_id>sl\_[a-zA-Z0-9\-]+)$',
        views.slide_details
    ),
    re_path(
        r'^create$',
        views.create_slide
    ),
    re_path(
        r'^$',
        views.list_slides
    )
]
