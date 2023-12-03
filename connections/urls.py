from django.urls import re_path
from connections import views

urlpatterns = [
    re_path(r'^sessions/oauth/google', views.authentication_view)
]
