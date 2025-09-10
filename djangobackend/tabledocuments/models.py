import pathlib
import uuid

from django.db import models
from django.db.models import Q
from django.db.models.constraints import CheckConstraint
from django.db.models.signals import post_delete
from django.dispatch import receiver
from tabledocuments.utils import upload_file_to, validate_file


class TableDocument(models.Model):
    """Represents a document stored in the database. A document
    is an element that contains metadata about a CSV/Excel/Google Sheet
    upload and its content"""

    document_uuid = models.UUIDField(
        default=uuid.uuid4
    )
    name = models.CharField(
        max_length=255
    )
    file = models.FileField(
        upload_to=upload_file_to,
        help_text="A csv, xls, xlsx, ods or json file.",
        validators=[validate_file],
        blank=True,
        null=True
    )
    column_names = models.JSONField(
        default=list,
        blank=True,
        help_text='A mapping of the column names present in the document'
    )
    column_options = models.JSONField(
        default=dict,
        blank=True,
        help_text=(
            'A mapping of column names to their visibility, editability, sortability '
            'and searchability for the final table presentation'
        )
    )
    column_types = models.JSONField(
        default=dict,
        blank=True,
        help_text=(
            'A mapping of column names to their data types. This is '
            'used to enforce data types when displaying the table.'
        )
    )
    url = models.URLField(
        max_length=500,
        help_text="The url that was used to request the file's content via HTTP",
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
        constraints = [
            CheckConstraint(
                check=Q(file__isnull=False) | Q(url__isnull=False),
                name='file_or_url_required'
            )
        ]

    def __str__(self):
        return self.name or str(self.document_uuid)


@receiver(post_delete, sender=TableDocument)
def delete_document_file(sender, instance, **kwargs):
    """Delete the file associated with the document when it is deleted."""
    if instance.file:
        path = pathlib.Path(instance.file.path)
        if path.exists() and path.is_file():
            path.unlink()
