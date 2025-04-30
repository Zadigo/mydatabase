# {
#     "access_token": "ya29.a0AfB_byDif7lSzxFR388y8N-f1YI5LJEISMP2HzwYJiEBQh2lsLw0HQZQ_pC8eu6XSKqxSHVE9s64V5GeTbZDe9HOdQoPC6GnYWoFl4ha4FtPzopHtSLMA1oU8LIyTJ6_e1kppeVupYiZamCNlbtsnVCBUDHRe9_X24TMaCgYKAWcSARASFQGOcNnCyib3SgHQH2HXWK8Z9xRseg0171",
#     "expires_in": 3599,
#     "refresh_token": "1//03JMppBuzqo3VCgYIARAAGAMSNwF-L9IrqK0xBApnyeR-1sHdB1Wqu4J6EtaFdgtkj6iDDUi9ZzK8DslM8fyDWOhiXQL080dKLp0",
#     "scope": "https://www.googleapis.com/auth/userinfo.profile openid https://www.googleapis.com/auth/userinfo.email",
#     "token_type": "Bearer",
#     "id_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjZmNzI1NDEwMWY1NmU0MWNmMzVjOTkyNmRlODRhMmQ1NTJiNGM2ZjEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI4MTg2NDQ1MDYzMzgtMzZzMHZiaWZpdm5iZ2s2bGdxYTQ5ajR2MW9zdWdzNXQuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI4MTg2NDQ1MDYzMzgtMzZzMHZiaWZpdm5iZ2s2bGdxYTQ5ajR2MW9zdWdzNXQuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMDAwODEzODY4Njc3NjI2MjU1MjkiLCJlbWFpbCI6InBlbmRlbnF1ZWpvaG5AZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImF0X2hhc2giOiJFNEh4VWlOTGRJcUdnYjFPUjZtbFJ3IiwibmFtZSI6IksgSm9obiIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NJcm1qTGJydXZyYm91SVY1TWRHWlpqZEUwcHBlUEZESm9MUzlaQm5WeDQ0cTdrPXM5Ni1jIiwiZ2l2ZW5fbmFtZSI6IksiLCJmYW1pbHlfbmFtZSI6IkpvaG4iLCJsb2NhbGUiOiJlbiIsImlhdCI6MTY5NTg1NjExMywiZXhwIjoxNjk1ODU5NzEzfQ.RAxdF8J59UlsP35LsZ5Jriegn6PRZa6sxtsk-tlpSy6b8ew1DTH5evZ4zxqlyinei4BQ4XvkG0bxiXR6gcrsrDhH6x6PiGgQy1eiDYez29T2Zw0n3XgBDuoFWFS3lM6bSvGqdt_SS5uDZvhezsHk1HnVst7OD61Vp6ESzhYGyEmx3DPfjKBkLpGTsN29Lt1sua9Vd-YyEfA5ctS9FS4JBeI1qF0M9iIh6RB59k0Sd1DnGf-LT_ZfkmpYwq23i5aASLmJmc-_XIDjHVdPoFcOVdxlPxJ_WrVzVWU1mQbRmILRQo4pVPe5sY6UBfBUijQi8bOU_H3Znvodnh3Yf5RV0g"
# }
from urllib.parse import parse_qs, unquote, urlparse

from connections.choices import TokenTypes
from connections.models import Connnection
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import fields
from rest_framework.serializers import Serializer
from rest_framework.views import Response


class AccessTokensSerializer(Serializer):
    id_token = fields.CharField()
    access_token = fields.CharField()
    expires_in = fields.IntegerField()
    refresh_token = fields.CharField()
    scope = fields.CharField()
    token_type = fields.CharField()

    def save(self, **kwargs):
        user = get_object_or_404(get_user_model(), id=1)
        instance = Connnection.objects.create(user=user, **self.validated_data)
        return Response({'state': True})


class GetExchangeCodeSerializer(Serializer):
    url = fields.URLField()

    def save(self, **kwargs):
        url = urlparse(unquote(self.validated_data['url']))
        params = parse_qs(url.query)
        return Response({'code': params['code'][0]})
