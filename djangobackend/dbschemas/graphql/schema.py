import graphene
from graphene_django.fields import DjangoListField
from graphql import GraphQLResolveInfo
from dbschemas.models import DatabaseProvider, DatabaseSchema
from dbschemas.graphql.utils import DatabaseProviderType, DatabaseSchemaType


class DatabaseSchemaQuery(graphene.ObjectType):
    all_dbschemas = DjangoListField(DatabaseSchemaType, name=graphene.String(required=False))
    db_schema_by_id = graphene.Field(DatabaseSchemaType, schema_id=graphene.Int(required=True))

    def resolve_all_dbschemas(root, info: GraphQLResolveInfo, name: str = None):
        qs = DatabaseSchema.objects.all()
        if name is not None:
            return qs.filter(name__icontains=name)
        return qs
    
    def resolve_db_schema_by_id(root, info: GraphQLResolveInfo, schema_id: int):
        return DatabaseSchema.objects.get(id=schema_id)
    
    def resolve_db_schema(root, info: GraphQLResolveInfo, id: int):
        database = DatabaseSchema.objects.get(id=id)
        return {'column_options': database.column_options, 'column_type_options': database.column_type_options}


class DatabaseProviderQuery(graphene.ObjectType):
    all_providers = DjangoListField(DatabaseProviderType)
    provider_by_id = graphene.Field(
        DatabaseProviderType,
        provider_id=graphene.Int(required=True),
        schema_id=graphene.Int(required=True)
    )

    def resolve_all_providers(root, info: GraphQLResolveInfo):
        return DatabaseProvider.objects.all()
    
    def resolve_provider_by_id(root, info: GraphQLResolveInfo, provider_id: int, schema_id: int):
        qs = DatabaseProvider.objects.filter(database_schema__id=schema_id)
        return qs.get(id=provider_id)
