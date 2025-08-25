from dbtables import choices
from django.db import models


class DatabaseTable(models.Model):
    """Represents a table in the user's database"""

    name = models.CharField(
        max_length=255,
        blank=False,
        null=False
    )
    description = models.TextField(
        max_length=1000
    )
    database_schema = models.ForeignKey(
        'dbschemas.DatabaseSchema',
        on_delete=models.CASCADE
    )
    documents = models.ManyToManyField(
        'tabledocuments.TableDocument',
        blank=True
    )
    component = models.CharField(
        max_length=100,
        choices=choices.TableComponentChoices.choices,
        default=choices.TableComponentChoices.DATA_TABLE
    )
    active = models.BooleanField(
        default=True
    )
    updated_at = models.DateTimeField(
        auto_now_add=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'database_schema'],
                name='unique_table_name_per_schema'
            )
        ]

    def __str__(self):
        return self.name
