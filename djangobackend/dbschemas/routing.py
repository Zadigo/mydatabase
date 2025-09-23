from django.urls import re_path
from dbschemas import consumers


urlpatterns = [
    re_path(r'ws/database$', consumers.DatabaseConsumer.as_asgi()),
]
