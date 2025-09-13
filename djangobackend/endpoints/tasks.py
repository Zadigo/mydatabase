from celery import shared_task


@shared_task
def create_hit(endpoint: str, db_resource: str, tbl_resource: str = None):
    pass
