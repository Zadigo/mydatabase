from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from django.utils.http import urlsafe_base64_encode


class DatabaseSchema(models.Model):
    """Represents a database which is collection
    of tables which themselves contain documents"""

    name = models.CharField(
        max_length=255,
        blank=False,
        null=False
    )
    database_functions = models.JSONField(
        default=list,
        blank=True,
        null=True
    )
    database_triggers = models.JSONField(
        default=list,
        blank=True,
        null=True
    )
    document_relationships = models.JSONField(
        default=list,
        blank=True,
        null=True
    )
    slug = models.SlugField(
        max_length=255,
        blank=True,
        null=True
    )
    updated_at = models.DateTimeField(
        auto_now_add=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'database schema'

    def __str__(self):
        return self.name

    @property
    def has_relationships(self) -> bool:
        return len(self.document_relationships) > 0

    @property
    def has_triggers(self):
        return len(self.database_triggers) > 0

    @property
    def has_functions(self):
        return len(self.database_functions) > 0

    @property
    def table_count(self):
        return self.databasetable_set.count()

    @property
    def has_tables(self):
        return self.table_count > 0


class DatabaseProvider(models.Model):
    """Stores keys and information about external providers
    like Airtable, Google Sheets, etc. from which the user
    can import data.
    """
    
    database_schema = models.ForeignKey(
        DatabaseSchema,
        models.CASCADE,
        help_text='The database schema that owns this provider'
    )
    google_sheet_api_key = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text='API key for accessing a public Google Sheet'
    )
    google_sheet_credentials = models.JSONField(
        default=dict,
        blank=True,
        null=True,
        help_text='Credentials for accessing a private Google Sheet'
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'database provider'

    def __str__(self):
        return 'Provider: ' + self.database_schema.name
    
    @property
    def has_google_sheet_connection(self):
        return bool(self.google_sheet_credentials)


@receiver(pre_save, sender=DatabaseSchema)
def create_table_slug(instance, **kwargs):
    if instance.slug is None or instance.slug == '':
        instance.slug = slugify(instance.name) + '-' + get_random_string(6)
    else:
        old_name_tokens = instance.slug.split('-')[:-1]
        if instance.name.lower().split(' ') != old_name_tokens:
            instance.slug = slugify(instance.name) + '-' + get_random_string(6)


@receiver(pre_save, sender=DatabaseProvider)
def encode_base64_api_key(instance, **kwargs):
    if instance.google_sheet_api_key:
        instance.google_sheet_api_key = urlsafe_base64_encode(instance.google_sheet_api_key.encode('utf-8')).decode('utf-8')
