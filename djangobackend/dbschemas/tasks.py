import datetime
import io

import pandas
import pytz
from celery import shared_task
from celery.utils.log import get_logger
from dbschemas.models import DatabaseSchema
from dbtables.models import DatabaseTable
from django.core.cache import cache
from django.core.files.base import ContentFile
from django.db.models import QuerySet
from tabledocuments.models import TableDocument

logger = get_logger(__name__)


@shared_task
def func_clean(document_uuid: str, columns: list[str], data: str, deep: bool = False) -> str:
    """Runs data cleaning operations on specified columns of the
    data provided in string format:
        - Trim whitespace
        - Normalize spaces (replace multiple spaces with a single space)
        - Convert to title case

    If deep is True, additional cleaning operations will be performed:
        - Remove special characters
    """
    buffer = io.StringIO(data)
    df = pandas.read_json(buffer)

    for column in columns:
        df[column] = df[column].str.strip()
        df[column] = df[column].str.replace(r'\s+', ' ', regex=True)
        df[column] = df[column].str.lower().str.title()

        if deep:
            df[column] = df[column].str.replace(
                r'[^a-zA-Z0-9\s]', '', regex=True)

    # In deep clean mode, normalize the dataframe columns
    # transform them in to lowercase + replace spaces with underscores
    if deep:
        df.columns = [col.lower().replace(' ', '_') for col in df.columns]

    try:
        instance = TableDocument.objects.get(uuid=document_uuid)
    except TableDocument.DoesNotExist:
        logger.error(
            f"TableDocument with uuid {document_uuid} does not exist.")
    else:
        instance.columns = df.columns.tolist()
        file = ContentFile(df.to_json(orient='records').encode('utf-8'))
        instance.file.save(f"{instance.name}.json", file)
        instance.save()

    return df.to_json(orient='records')


@shared_task
def func_count(columns: list[str], data: str):
    pass


@shared_task
def func_sum(columns: list[str], data: str):
    pass


@shared_task
def func_avg(columns: list[str], data: str):
    pass


@shared_task
def func_min(columns: list[str], data: str):
    pass


@shared_task
def func_max(columns: list[str], data: str):
    pass


@shared_task
def func_upper(columns: list[str], data: str) -> str:
    """Convert specified columns to uppercase."""
    buffer = io.StringIO(data)

    df = pandas.read_json(buffer)
    for column in columns:
        df[column] = df[column].str.upper()

    return df.to_json(orient='records')


@shared_task
def func_lower(columns: list[str], data: str) -> str:
    """Convert specified columns to lowercase."""
    buffer = io.StringIO(data)

    df = pandas.read_json(buffer)
    for column in columns:
        df[column] = df[column].str.lower()

    return df.to_json(orient='records')


@shared_task
def func_title(columns: list[str], data: str) -> str:
    """Convert specified columns to title case."""
    buffer = io.StringIO(data)

    df = pandas.read_json(buffer)
    for column in columns:
        df[column] = df[column].str.lower().str.title()

    return df.to_json(orient='records')


@shared_task
def func_length(columns: list[str], data: str):
    pass


@shared_task
def func_trim(columns: list[str], data: str, **kwargs: str) -> str:
    """Trim whitespace from specified columns."""
    buffer = io.StringIO(data)

    df = pandas.read_json(buffer)
    for column in columns:
        df[column] = df[column].str.strip()

    # normalize = kwargs.get('normalize', False)
    # if normalize:
    #     for column in columns:
    #         df[column] = df[column].str.replace(r'\s+', ' ', regex=True)

    return df.to_json(orient='records')


@shared_task
def func_group_concat(columns: list[str], data: str):
    pass


@shared_task
def func_coalesce(columns: list[str], data: str):
    pass


@shared_task
def func_extract(columns: list[str], data: str, **kwargs: str) -> str:
    buffer = io.StringIO(data)
    df = pandas.read_json(buffer)

    value_to_extract = kwargs.get('value_to_extract', None)

    if value_to_extract is not None:
        for column in columns:
            pass


@shared_task
def func_now(data: str, **kwargs: str) -> str:
    """Add a new column 'now' with the current timestamp."""
    buffer = io.StringIO(data)
    df = pandas.read_json(buffer)

    timezone_str = kwargs.get('timezone', 'UTC')
    df['now'] = datetime.datetime.now(pytz.timezone(timezone_str)).isoformat()

    return df.to_json(orient='records')


@shared_task
def func_date(columns: list[str], data: str, **kwargs: str) -> str:
    pass


@shared_task
def func_time(columns: list[str], data: str, **kwargs: str) -> str:
    pass


@shared_task
def func_datetime(columns: list[str], data: str, **kwargs: str) -> str:
    pass


@shared_task
def func_strftime(columns: list[str], data: str, **kwargs: str) -> str:
    pass


@shared_task
def func_current_timestamp(data: str, **kwargs: str) -> str:
    """Add a new column 'timestamp' with the current timestamp."""
    buffer = io.StringIO(data)
    df = pandas.read_json(buffer)

    timezone_str = kwargs.get('timezone', 'UTC')
    df['timestamp'] = datetime.datetime.now(
        pytz.timezone(timezone_str)).timestamp()

    return df.to_json(orient='records')


@shared_task
def func_current_date(data: str, **kwargs: str) -> str:
    """Add a new column 'date' with the current date."""
    buffer = io.StringIO(data)
    df = pandas.read_json(buffer)

    timezone_str = kwargs.get('timezone', 'UTC')
    df['date'] = datetime.datetime.now(
        pytz.timezone(timezone_str)).date().isoformat()

    return df.to_json(orient='records')


@shared_task
def func_current_time(data: str, **kwargs: str) -> str:
    buffer = io.StringIO(data)
    df = pandas.read_json(buffer)

    timezone_str = kwargs.get('timezone', 'UTC')
    df['datetime'] = datetime.datetime.now(
        pytz.timezone(timezone_str)).isoformat()

    return df.to_json(orient='records')


@shared_task
def func_random(data: str, **kwargs: str) -> str:
    pass


@shared_task
def func_md5(columns: list[str], data: str, **kwargs: str) -> str:
    pass


@shared_task
def func_sha256(columns: list[str], data: str, **kwargs: str) -> str:
    pass


@shared_task
def func_sha512(columns: list[str], data: str, **kwargs: str) -> str:
    pass


FUNCTION_MAP = {
    'clean': func_clean,
    'count': func_count,
    'sum': func_sum,
    'avg': func_avg,
    'min': func_min,
    'max': func_max,
    'upper': func_upper,
    'lower': func_lower,
    'title': func_title,
    'length': func_length,
    'trim': func_trim,
    'group_concat': func_group_concat,
    'coalesce': func_coalesce,
    'extract': func_extract,
    'now': func_now,
    'date': func_date,
    'time': func_time,
    'datetime': func_datetime,
    'strftime': func_strftime,
    'current_timestamp': func_current_timestamp,
    'current_date': func_current_date,
    'current_time': func_current_time,
    'random': func_random,
    'md5': func_md5,
    'sha256': func_sha256,
    'sha512': func_sha512
}


@shared_task
def prefetch_relationships(database_id: str):
    """Function that reads the documents and creates an association that
    is then stored in Redis cache for quick retrieval when needed.

    The direction parameter indicates the type of relationship:
        - '1-1': one-to-one"""

    database = DatabaseSchema.objects.get(id=database_id)

    tables: QuerySet[DatabaseTable] = database.databasetable_set.all()

    for item in database.document_relationships:
        table1 = tables.get(id=item['from_table'])
        table2 = tables.get(id=item['to_table'])

        if table1.active_document_datasource is None or table2.active_document_datasource is None:
            logger.error(
                "One of the tables does not have an active document datasource.")
            return

        doc1 = table1.documents.get(
            document_uuid=table1.active_document_datasource)
        doc2 = table2.documents.get(
            document_uuid=table2.active_document_datasource)

        df1 = pandas.read_json(io.StringIO(doc1.file.read().decode('utf-8')))
        df2 = pandas.read_json(io.StringIO(doc2.file.read().decode('utf-8')))

        # Depending on the direction, create the relationship
        if item['meta_definitions']['type'] == '1-1':
            df = pandas.merge(df1, df2, how='inner',
                              left_index=True, right_index=True)
            cache.set(item['name'], df.to_json(orient='records'), timeout=None)
            logger.info(
                f"One-to-one relationship created between {table1.name} and {table2.name}.")
