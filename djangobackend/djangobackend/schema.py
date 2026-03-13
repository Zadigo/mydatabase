import graphene
from tabledocuments.schema import TableDocumentsQuery

class Query(TableDocumentsQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
