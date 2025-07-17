from django.db.models import Choices


class AccessChoices(Choices):
    PUBLIC = 'Public'
    PRIVATE = 'Private'


class ComponentTypes(Choices):
    TABLE_BLOCK = 'table-block'
    GRAPH_BLOCK = 'graph-block'
    GRID_BLOCK = 'grid-block'
    CHART_BLOCK = 'chart-block'


class OperatorChoices(Choices):
    CONTAINS = 'contains'
    DOES_NOT_CONTAIN = 'does not contain'
    IS = 'is'
    IS_NOT = 'is not'
    IS_EMPTY = 'is empty'
    IS_NOT_EMPTY = 'is not empty'
    EQUALS = 'equals'
    IS_NOT_EQUAL = 'is not equal'
    GREATER_THAN = 'greater than'
    GREATER_THAN_OR_EQUAL_TO = 'greather than or equal to'
    LESS_THAN = 'less than'
    LESS_THAN_OR_EQUAL_TO = 'less than or equal to'


class InputTypeChoices(Choices):
    INPUT = 'Input'
    SINGLE_SELECT = 'Single select'
    MULTI_SELECT = 'Multi select'
    DATE = 'Date'


class UnionChoices(Choices):
    AND = 'and'
    OR = 'or'


class ColumnTypeChoices(Choices):
    TEXT = 'Text'
    DATE = 'Date'
    LINK = 'Link'
    NUMBER = 'Number'


class SortingChoices(Choices):
    NO_SORT = 'No sort'
    ASCENDING = 'Ascending'
    DESCENDING = 'Descending'
