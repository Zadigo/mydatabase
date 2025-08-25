
from django.db import models


class DatabaseSchema(models.Model):
    """Represents a database which is collection
    of tables which themselves contain documents"""

    name = models.CharField(
        max_length=255,
        blank=False,
        null=False
    )
    updated_at = models.DateTimeField(
        auto_now_add=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.name
