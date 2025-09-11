from django.urls import re_path
from dbschemas.api import views

app_name = 'dbschemas'

urlpatterns = [
    re_path(
        r'^(?P<pk>\d+)/restart$',
        views.RestartProject.as_view(),
        name='restart_database'
    ),
    re_path(
        r'^(?P<pk>\d+)/delete$',
        views.DeleteDatabase.as_view(),
        name='delete_database'
    ),
    re_path(
        r'^(?P<pk>\d+)/endpoints$',
        views.ListDatabaseEndpoints.as_view(),
        name='list_database_endpoints'
    ),
    re_path(
        r'^(?P<pk>\d+)$',
        views.UpdateDatabase.as_view(),
        name='retrieve_update_database'
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
