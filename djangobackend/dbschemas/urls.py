from django.urls import re_path
from dbschemas.api import views

app_name = 'dbschemas'

urlpatterns = [
    re_path(
        r'^(?P<pk>\d+)/delete$',
        views.DeleteDatabase.as_view(),
        name='delete_database'
    ),
    re_path(
        r'^create$',
        views.CreateDatabase.as_view(),
        name='create_database'
    ),
    re_path(
        r'^$',
        views.ListDatabases.as_view(),
        name='list_databases'
    )
]
