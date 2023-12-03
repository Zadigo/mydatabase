from django.urls import re_path
from connections.api import views

urlpatterns = [
    re_path(r'^authenticate', views.create_authentication_view),
    re_path(r'^exchange', views.unquote_url_view),
    re_path(r'^decode$', views.unquote_url_view)
]
