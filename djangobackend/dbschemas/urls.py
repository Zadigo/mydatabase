from django.urls import re_path
from dbschemas.api import views

app_name = 'dbschemas'

urlpatterns = [
    re_path(
        r'^databases/$',
        views.ListDatabases.as_view(),
        name='list_databases'
    )
]
