from django.urls import re_path
from tabledocuments import consumers

urlpatterns = [
    re_path(
        r'^ws/databases/(?P<database_id>\d+)/documents$',
        consumers.DocumentEditionConsumer.as_asgi()
    )
]
