from django.urls import re_path
from datasources.api import views

app_name = 'datasource_api'

urlpatterns = [
    re_path(
        r'^webhook/(?P<webhook_id>wk\_[a-zA-Z0-9\-]+)$',
        views.send_to_webhook,
        name='webhook_send'
    ),
    re_path(
        r'^(?P<data_source_id>ds_[a-zA-Z0-9]+)/remove$',
        views.delete_data_source,
        name='delete'
    ),
    re_path(
        r'^(?P<data_source_id>ds\_[a-zA-Z0-9]+)/columns$',
        views.UpdateColumnDataTypes.as_view(),
        name='column_data_types'
    ),
    re_path(
        r'^(?P<data_source_id>ds\_[a-zA-Z0-9]+)$',
        views.LoadDataSource.as_view(),
        name='load'
    ),
    re_path(
        r'^upload$',
        views.UploadDataSource.as_view(),
        name='upload'
    ),
    re_path(
        r'^$',
        views.ListDataSources.as_view(),
        name='list'
    )
]
