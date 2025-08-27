from django.urls import re_path
from dbtables.api import views

app_name = 'database_tables'

urlpatterns = [
    re_path(
        r'^tables/(?P<pk>\d+)/upload$',
        views.UploadNewDocument.as_view(),
        name='upload_document'
    ),
    re_path(
        r'^tables/(?P<pk>\d+)$',
        views.UpdateTable.as_view(),
        name='update_table'
    )
]
