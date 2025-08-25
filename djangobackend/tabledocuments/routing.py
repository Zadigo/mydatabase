from django.urls import re_path
from tabledocuments import consumers

urlpatterns = [
    re_path(
        r'documents/', 
        consumers.DatabaseConsumer.as_asgi()
    )
]
