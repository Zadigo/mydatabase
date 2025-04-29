from django.urls import re_path
from datasources.api import views

urlpatterns = [
    re_path(
        r'^webhook/(?P<webhook_id>wk\_[a-zA-Z0-9\-]+)$',
        views.send_to_webhook
    ),
    re_path(
        r'^(?P<data_source_id>ds_[a-zA-Z0-9]+)/remove$',
        views.delete_data_source
    ),
    re_path(
        r'^(?P<data_source_id>ds\_[a-zA-Z0-9]+)/columns$',
        views.update_column_data_types
    ),
    re_path(
        r'^(?P<data_source_id>ds\_[a-zA-Z0-9]+)$',
        views.load_data_source_data
    ),
    re_path(
        r'^upload$',
        views.upload_new_data_source
    ),
    re_path(
        r'^$',
        views.list_user_data_sources
    )
]
