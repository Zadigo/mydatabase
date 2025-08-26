from celery import shared_task

@shared_task
def update_document_relationship(lh_document_id: str, rh_document_id: str, relationship_fields: list[str]=[], select: list[str] = []):
    # Your document relationship update logic here
    pass


@shared_task
def get_google_sheet_data(sheet_id: str, range_name: str):
    # Your Google Sheets API fetching logic here
    pass


@shared_task
def get_airtable_data(base_id: str, table_name: str, view_name: str):
    # Your Airtable API fetching logic here
    pass
