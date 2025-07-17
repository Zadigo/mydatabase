from rest_framework.decorators import api_view
from connections.api import serializers
import requests


@api_view(http_method_names=['post'])
def unquote_url_view(request, **kwargs):
    serializer = serializers.GetExchangeCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    # base_url = 'https://oauth2.googleapis.com/token'
    # headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    # scope = [
    #     'https://www.googleapis.com/auth/userinfo.profile',
    #     'https://www.googleapis.com/auth/userinfo.email'
    # ]
    # options = {
    #     'redirect_uri': 'http://localhost:8080/rest/oauth2-credential/callback',
    #     'client_id': '818644506338-36s0vbifivnbgk6lgqa49j4v1osugs5t.apps.googleusercontent.com',
    #     'access_type': 'offline',
    #     'response_type': 'code',
    #     'prompt': 'consent',
    #     'scope': ' '.join(scope)
    # }
    # response = requests.post(base_url, data=options, headers=headers)
    return serializer.save()


@api_view(http_method_names=['post'])
def create_authentication_view(request, **kwargs):
    serializer = serializers.AccessTokensSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return serializer.save()


# base_url = 'https://oauth2.googleapis.com/token'
# headers = {'Content-Type': 'application/x-www-form-urlencoded'}
# scope = [
#     'https://www.googleapis.com/auth/userinfo.profile',
#     'https://www.googleapis.com/auth/userinfo.email',
#     'https://www.googleapis.com/auth/spreadsheets.readonly'
# ]
# options = {
#     'redirect_uri': 'http://localhost:8080/rest/oauth2-credential/callback',
#     'client_id': '818644506338-36s0vbifivnbgk6lgqa49j4v1osugs5t.apps.googleusercontent.com',
#     'access_type': 'offline',
#     'response_type': 'code',
#     'prompt': 'consent',
#     'scope': ' '.join(scope)
# }
# response = requests.post(base_url, data=options, headers=headers)
# print(response.json())
