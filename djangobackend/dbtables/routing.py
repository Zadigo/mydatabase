from django.urls import re_path
from dbtables import consumers


urlpatterns = [
    re_path(
        r'^ws/tables/(?P<table_id>\d+)$', 
        consumers.TableCreationConsumer.as_asgi(),
        name='table_creation_consumer'
    )
]
