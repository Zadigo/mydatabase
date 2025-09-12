
from django.db import models


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
