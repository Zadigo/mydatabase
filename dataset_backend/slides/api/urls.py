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
        views.DeleteBlock.as_view(),
        name='delete_block'
    ),
    re_path(
        r'^(?P<slide_id>sl\_[a-zA-Z0-9\-]+)/blocks/(?P<block_id>bl\_[a-zA-Z0-9\-]+)$',
        views.GetBlock.as_view(),
        name='block'
    ),
    re_path(
        r'^(?P<slide_id>sl\_[a-zA-Z0-9\-]+)/blocks/create$',
        views.CreateBlock.as_view(),
        name='create_block'
    ),
    re_path(
        r'^(?P<slide_id>sl\_[a-zA-Z0-9\-]+)/update$',
        views.UpdateSlide.as_view(),
        name='update'
    ),
    re_path(
        r'^(?P<slide_id>sl\_[a-zA-Z0-9\-]+)/final$',
        views.view_final_slide,
        name='final_slide'
    ),
    re_path(
        r'^(?P<slide_id>sl\_[a-zA-Z0-9\-]+)$',
        views.SlideDetails.as_view(),
        name='details'
    ),
    re_path(
        r'^create$',
        views.CreateSlide.as_view(),
        name='create'
    ),
    re_path(
        r'^$',
        views.ListSlides.as_view(),
        name='list'
    )
]
