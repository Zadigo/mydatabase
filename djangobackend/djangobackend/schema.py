import graphene
from tabledocuments.schema import TableDocumentsQuery
from dbschemas.schema import DbSchemaQuery, DatabaseProviderQuery
from dbtables.schema import DatabaseTableQuery
from dbschemas.schema import CreateDatabaseMutation
# from accounts.schema import AccountsQuery

class Query(DatabaseTableQuery, DatabaseProviderQuery, DbSchemaQuery, TableDocumentsQuery, graphene.ObjectType):
    pass


class Mutation(graphene.ObjectType):
    create_database = CreateDatabaseMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
