from celery import shared_task
from datasources.models import DataSource

@shared_task
def clean_csv_file(source_id: str):
    instance = DataSource.objects.get(data_source_id=source_id)
    