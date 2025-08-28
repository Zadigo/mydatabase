from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.utils.crypto import get_random_string


def upload_file_to(instance, filename):
    timesptamp = timezone.now().timestamp()
    extension = filename.split('.')[-1]
    new_filename = f"doc--{instance.document_uuid}__{timesptamp}.{extension}"
    return f"table_documents/{new_filename}"


def validate_file(name):
    """We only accept csv, xls, xlsx and ods files. We
    also allow json files but they will be transformed
    back to a csv format"""
    validator = FileExtensionValidator(allowed_extensions=['csv', 'xls', 'xlsx', 'ods', 'json'])
    validator(name)
