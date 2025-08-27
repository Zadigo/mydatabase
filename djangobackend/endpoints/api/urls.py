from django.urls import re_path
from endpoints import views

app_name = 'endpoints'

urlpatterns = [
    re_path(
        r'^api/secret/(?P<endpoint>[^/]+)/?$',
        views.SecretApiEndpointRouter.as_view(),
        name='secret-api-endpoint'
    ),
    re_path(
        r'^api/public/(?P<endpoint>[^/]+)/(?P<database>[a-z\-]+)/(?P<table>[a-z\-]+)$',
        views.PublicApiEndpointRouter.as_view(),
        name='table-level-endpoint'
    ),
    re_path(
        r'^api/public/(?P<endpoint>[^/]+)/(?P<database>[a-z\-]+)$',
        views.PublicApiEndpointRouter.as_view(),
        name='database-level-endpoint'
    )
]
