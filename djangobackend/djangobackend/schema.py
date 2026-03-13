import graphene
from tabledocuments.schema import TableDocumentsQuery
from dbschemas.schema import DbSchemaQuery, DatabaseProviderQuery
from dbtables.schema import DatabaseTableQuery

class Query(DatabaseTableQuery, DatabaseProviderQuery, DbSchemaQuery, TableDocumentsQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
