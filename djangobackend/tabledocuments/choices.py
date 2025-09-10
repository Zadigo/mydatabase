from django.db.models import TextChoices


class ColumnTypes(TextChoices):
    STRING = 'String', 'String'
    NUMBER = 'Number', 'Number'
    BOOLEAN = 'Boolean', 'Boolean'
    DATE = 'Date', 'Date'
    DATETIME = 'DateTime', 'DateTime'
    ARRAY = 'Array', 'Array'
    DICT = 'Dict', 'Dict'
