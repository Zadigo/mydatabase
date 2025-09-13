from django.urls import re_path
from endpoints.api import views

app_name = 'endpoints'

urlpatterns = [
    re_path(
        r'^secret/(?P<endpoint>[^/]+)$',
        views.SecretApiEndpointRouter.as_view(),
        name='secret-api-endpoint'
    ),
    re_path(
        r'^public/(?P<database>\d+)/table/(?P<table>\d+)/(?P<endpoint>[a-z\-]+)$',
        views.PublicApiEndpointRouter.as_view(),
        name='table-level-endpoint'
    ),
    re_path(
        r'^public/(?P<database>\d+)/(?P<endpoint>[a-z\-]+)$',
        views.PublicApiEndpointRouter.as_view(),
        name='database-level-endpoint'
    ),
    re_path(
        r'^(?P<database>\d+)/create$',
        views.CreateEndpoint.as_view(),
        name='create'
    ),
    re_path(
        r'^$',
        views.ListEndpoints.as_view(),
        name='list-endpoints'
    )
]
