import pandas
from celery import shared_task
from sheets.models import Sheet


@shared_task
def sheet_columns(sheet_id: str):
    try:
        sheet = Sheet.objects.get(sheet_id=sheet_id)
    except Sheet.DoesNotExist:
        return {'error': 'Sheet not found'}
    else:
        if sheet.csv_based:
            if not sheet.csv_file:
                return []
            df = pandas.read_csv(sheet.csv_file.path)
            sheet.columns = df.columns.tolist()
            sheet.save()
            return sheet.columns
