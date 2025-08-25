from django.db import models

class TableDocument(models.Model):
    """Represents a document stored in the database. A document
    is an element that contains metadata about a CSV/Excel/Google Sheet
    upload and its content"""

    name = models.CharField(
        max_length=255
    )
    file = models.FileField(
        upload_to='table_documents/'
    )
    updated_at = models.DateTimeField(
        auto_now_add=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.name
