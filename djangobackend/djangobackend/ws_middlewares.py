from typing import TYPE_CHECKING, Any
from django.contrib.auth.models import AnonymousUser, User
from rest_framework.authtoken.models import Token
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware



@database_sync_to_async
def get_user(token_key: str) -> AnonymousUser | User:
    try:
        token = Token.objects.get(key=token_key)
        return token.user
    except Token.DoesNotExist:
        return AnonymousUser()


class JWTTokenAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        # headers = dict(scope['headers'])
        # print('headers', headers)
        # if b'authorization' in headers:
        #     try:
        #         token_name, token_key = headers[b'authorization'].decode().split()
        #         if token_name == 'Token':
        #             scope['user'] = get_user(token_key)
        #     except Token.DoesNotExist:
        #         scope['user'] = AnonymousUser()

        token = scope.get('token', None)
        if token is None:
            scope['user'] = AnonymousUser()
        else:
            try:
                name, key = token.decode().split()
                if name == 'Token':
                    scope['user'] = get_user(key)
            except Token.DoesNotExist:
                scope['user'] = AnonymousUser()

        return await self.inner(scope, receive, send)
