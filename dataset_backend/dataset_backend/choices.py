from django.db.models import Choices


class ColumnTypeChoices(Choices):
    TEXT = 'Text'
    DATE = 'Date'
    LINK = 'Link'
    NUMBER = 'Number'
