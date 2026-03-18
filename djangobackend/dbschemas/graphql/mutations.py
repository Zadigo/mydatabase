import graphene
from graphql import GraphQLResolveInfo
from dbschemas.models import DatabaseSchema
from dbschemas.graphql.schema import DatabaseSchemaType

class CreateDatabaseSchemaMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    db_schema = graphene.Field(DatabaseSchemaType)

    @classmethod
    def mutate(cls, root, info: GraphQLResolveInfo, name: str):
        instance = DatabaseSchema.objects.create(name=name)
        return CreateDatabaseSchemaMutation(db_schema=instance)


class UpdateDatabaseSchemaMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String(required=False)

    db_schema = graphene.Field(DatabaseSchemaType)

    @classmethod
    def mutate(cls, root, info: GraphQLResolveInfo, id: int, name: str = None):
        instance = DatabaseSchema.objects.get(pk=id)

        instance.name = name or instance.name
        instance.save()
        
        return UpdateDatabaseSchemaMutation(db_schema=instance)
