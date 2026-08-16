import enum

from django.db import models


class TableComponentChoices(models.TextChoices):
    DATA_TABLE = 'data-table'
    GRAPH_TABLE = 'graph-table'


class TableWebSocketActions(enum.Enum):
    CHECKOUT_URL = 'checkout_url'
    CHECKOUT_FILE = 'checkout_file'
