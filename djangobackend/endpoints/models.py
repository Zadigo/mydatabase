import uuid

from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from endpoints import validators
from endpoints.utils import create_endpoint


class ApiEndpoint(models.Model):
    """This class provides functionnalities so that users
    external or internal can interact with databases.

    An endpoint can be public or private (only accessible from 
    an organization standpoint) depending on the user's preferences
    """

    database_schema = models.ForeignKey(
        'dbschemas.DatabaseSchema',
        models.CASCADE,
        null=True,
    )
    endpoint_uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True
    )
    endpoint = models.CharField(
        max_length=200,
        unique=True,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.endpoint_uuid)


class PublicApiEndpoint(ApiEndpoint):
    public_key = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text=(
            "Public key allows external users to run operations on "
            "the data of authorized database (create, update, delete...)"
        )
    )
    bearer_token = models.CharField(
        max_length=200,
        help_text="Bearer token allows external users to authenticate their requests",
        blank=True,
        null=True
    )
    methods = models.JSONField(
        default=list,
        validators=[validators.validate_http_method]
    )


class SecretApiEndpoint(ApiEndpoint):
    secret_key = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text=(
            "Secret key allows the database creator to run internal "
            "operations on his databases (create, delete...) or modify "
            "instance parameters and should never be shared"
        )
    )
    private = models.BooleanField(
        default=False
    )


@receiver(pre_save, sender=PublicApiEndpoint)
def create_public_endpoint(instance, **kwargs):
    if not instance.public_key:
        instance.public_key = create_endpoint('public')


@receiver(pre_save, sender=SecretApiEndpoint)
def create_secret_endpoint(instance, **kwargs):
    if not instance.secret_key:
        instance.secret_key = create_endpoint('secret')


@receiver(pre_save, sender=PublicApiEndpoint)
def create_bearer_token(instance, **kwargs):
    """The bearer token is a random string of 32 characters
    that will be used to authenticate requests to the public API endpoint."""
    if not instance.bearer_token:
        instance.bearer_token = get_random_string(32)


@receiver(post_save, sender=PublicApiEndpoint)
def set_http_methods(instance, created, **kwargs):
    """The http methods are used to define what kind of operations
    can be done on the endpoint. If no method is specified,
    we set all methods by default."""
    if created:
        if not instance.methods:
            instance.methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']
            instance.save()
