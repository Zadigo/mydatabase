import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.timezone import now

from connections import choices

USER_MODEL = get_user_model()


class Connnection(models.Model):
    """Stores user access connections to a Google sheet"""

    user = models.ForeignKey(
        USER_MODEL,
        models.CASCADE
    )
    id_token = models.CharField(
        max_length=1000,
        blank=True,
        null=True
    )
    access_token = models.CharField(
        max_length=500,
        blank=True,
        null=True
    )
    refresh_token = models.CharField(
        max_length=300,
        blank=True,
        null=True
    )
    expires_in = models.PositiveIntegerField()
    token_type = models.CharField(
        max_length=50,
        choices=choices.TokenTypes.choices,
        default=choices.TokenTypes.BEARER
    )
    scope = models.CharField(
        max_length=500,
        blank=True,
        null=True
    )
    created_on = models.DateTimeField(default=now)

    def __str__(self):
        return f'Connection for {self.user}'

    @property
    def expired(self):
        current_date = now()
        expiration_date = datetime.timedelta(
            seconds=self.expires_in) + self.created_on
        return current_date > expiration_date
