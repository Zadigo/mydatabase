from celery import shared_task
import requests
import pandas
from tabledocuments.models import TableDocument
from django.core.files.base import ContentFile
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task
def request_document_by_url(url: str, headers: dict[str, str] = {}):
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        if 'application/json' in response.headers.get('Content-Type', ''):
            return response.json()

        if 'application/csv' in response.headers.get('Content-Type', ''):
            # .splitlines()
            return response.text
    return None


@shared_task
def create_csv_file_from_data(data, document_id):
    if data is None:
        return

    print(TableDocument.objects.all())

    try:
        document = TableDocument.objects.get(id=document_id)
    except TableDocument.DoesNotExist:
        logger.error(f"Document with ID {document_id} does not exist.")
    else:
        if isinstance(data, str):
            content = ContentFile(data)
            document.file.save(f'{document.name}.csv', content)
            document.save()

        if isinstance(data, list):
            df = pandas.DataFrame(data)
            csv_content = df.to_csv(index=False)
            content = ContentFile(csv_content)
            document.file.save(f'{document.name}.csv', content)
            document.save()
