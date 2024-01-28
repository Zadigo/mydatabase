from django.urls import re_path
from sheets.api import views

urlpatterns = [
    re_path(
        r'^webhook/(?P<webhook_id>wk\_[a-zA-Z0-9\-]+)$',
        views.send_to_webhook
    ),
    re_path(
        r'^(?P<sheet_id>sh_[a-zA-Z0-9]+)/remove$',
        views.delete_csv_file
    ),
    re_path(
        r'^(?P<sheet_id>sh\_[a-zA-Z0-9]+)/columns$',
        views.update_column_data_types
    ),
    re_path(
        r'^(?P<sheet_id>sh\_[a-zA-Z0-9]+)$',
        views.load_csv_file_data
    ),
    re_path(
        r'^upload$',
        views.upload_csv_file
    ),
    re_path(
        r'^$',
        views.user_sheets
    )
]
