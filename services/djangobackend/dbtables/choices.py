from django.db import models 


class TableComponentChoices(models.TextChoices):
    DATA_TABLE = 'data-table'
    GRAPH_TABLE = 'graph-table'
