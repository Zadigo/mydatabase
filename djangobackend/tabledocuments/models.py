import uuid

from django.db import models
from django.db.models import Q
from django.db.models.constraints import CheckConstraint
from tabledocuments.utils import upload_file_to, validate_file


class TableDocument(models.Model):
    """Represents a document stored in the database. A document
    is an element that contains metadata about a CSV/Excel/Google Sheet
    upload and its content"""

    document_uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(
        max_length=255
    )
    file = models.FileField(
        upload_to=upload_file_to,
        help_text="A csv, xls, xlsx, ods or json file.",
        validators=[
            validate_file
        ],
        blank=True,
        null=True
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
