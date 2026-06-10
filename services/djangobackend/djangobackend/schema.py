import graphene

from dbschemas.graphql import mutations as dbschemas_mutations
from dbschemas.graphql import schema as dbschemas_schema
from tabledocuments.graphql import schema as tabledocuments_schema
from tabledocuments.graphql import mutations as tabledocuments_mutations
from dbtables.graphql import schema as dbtables_schema

class Query(
    dbschemas_schema.DatabaseProviderQuery, 
    dbschemas_schema.DatabaseSchemaQuery,
    tabledocuments_schema.TableDocumentsQuery,
    dbtables_schema.DatabaseTableQuery,
    graphene.ObjectType
):
    pass


class Mutation(graphene.ObjectType):
    create_database = dbschemas_mutations.CreateDatabaseSchemaMutation.Field()
    update_database = dbschemas_mutations.UpdateDatabaseSchemaMutation.Field()
    update_table_document = tabledocuments_mutations.MutateTableDocument.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
