from django.db.models import Choices

class TokenTypes(Choices):
    BEARER = 'Bearer'
