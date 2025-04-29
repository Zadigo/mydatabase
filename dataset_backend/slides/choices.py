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
    CONTAINS = 'Contains'
    DOES_NOT_CONTAIN = 'Does not contain'
    IS = 'Is'
    IS_NOT = 'Is not'
    IS_EMPTY = 'Is empty'
    IS_NOT_EMPTY = 'Is not empty'
    EQUALS = 'Equals'
    IS_NOT_EQUAL = 'Is not equal'
    GREATER_THAN = 'Greater than'
    GREATER_THAN_OR_EQUAL_TO = 'Greather than or equal to'
    LESS_THAN = 'Less than'
    LESS_THAN_OR_EQUAL_TO = 'Less than or equal to'


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
