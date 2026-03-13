import graphene
from tabledocuments.schema import TableDocumentsQuery
from dbschemas.schema import DbSchemaQuery, DatabaseProviderQuery

class Query(DatabaseProviderQuery, DbSchemaQuery, TableDocumentsQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
