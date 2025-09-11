from django.urls import re_path
from endpoints.api import views

app_name = 'endpoints'

urlpatterns = [
    re_path(
        r'^api/secret/(?P<endpoint>[^/]+)/?$',
        views.SecretApiEndpointRouter.as_view(),
        name='secret-api-endpoint'
    ),
    re_path(
        r'^api/public/(?P<endpoint>[a-z\-]+)/(?P<database>\d+)/(?P<table>\d+)$',
        views.PublicApiEndpointRouter.as_view(),
        name='table-level-endpoint'
    ),
    re_path(
        r'^api/public/(?P<endpoint>[a-z\-]+)/(?P<database>\d+)$',
        views.PublicApiEndpointRouter.as_view(),
        name='database-level-endpoint'
    ),
    re_path(
        r'^$',
        views.ListEndpoints.as_view(),
        name='list-endpoints'
    )
]
