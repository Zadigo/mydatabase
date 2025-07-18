from django.urls import path, re_path
from slides import consumers

websocket_urlpatterns = [
    re_path(
        r'^ws/slides$',
        consumers.SlideConsumer.as_asgi()
    )
]
