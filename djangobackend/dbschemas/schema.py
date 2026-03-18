import graphene
from graphene_django.types import DjangoObjectType
from graphene_django.fields import DjangoListField
from graphql import GraphQLResolveInfo
from django.db.models import QuerySet
from dbschemas.models import DatabaseProvider, DatabaseSchema

class DatabaseSchemaType(DjangoObjectType):
    has_relationships = graphene.Boolean()
    has_triggers = graphene.Boolean()
    has_functions = graphene.Boolean()
    table_count = graphene.Int()
    has_tables = graphene.Boolean()

    class Meta:
        model = DatabaseSchema
        fields = [
            'id',
            'name',
            'database_functions',
            'database_triggers',
            'document_relationships',
            'slug',
            'updated_at',
            'created_at'
        ]
        field_fields = {
            'name': ['exact', 'icontains']
        }
        
    @classmethod
    def get_queryset(cls, queryset: QuerySet[DatabaseSchema], info: GraphQLResolveInfo):
        # if info.context.user.is_anonymous:
        #     return queryset.none()
        # return queryset.filter(user=info.context.user)
        return queryset.all()
    

class DatabaseProviderType(DjangoObjectType):
    class Meta:
        model = DatabaseProvider
        fields = [
            'id',
            'database_schema',
            'document_relationships',
            'updated_at',
            'created_at'
        ]
        field_fields = {
            'database_schema__name': ['exact', 'icontains']
        }

    @classmethod
    def get_queryset(cls, queryset: QuerySet[DatabaseProvider], info: GraphQLResolveInfo):
        # if info.context.user.is_anonymous:
        #     return queryset.none()
        # providers = queryset.prefetch_related('database_schema').all()
        # return providers.filter(database_schema__user=info.context.user)
        return queryset.all()


class DbSchemaQuery(graphene.ObjectType):
    all_dbschemas = DjangoListField(DatabaseSchemaType, name=graphene.String(required=False))
    db_schema_by_id = graphene.Field(DatabaseSchemaType, schema_id=graphene.Int(required=True))

    def resolve_all_dbschemas(root, info: GraphQLResolveInfo, name: str = None):
        qs = DatabaseSchema.objects.all()
        if name is not None:
            return qs.filter(name__icontains=name)
        return qs
    
    def resolve_db_schema_by_id(root, info: GraphQLResolveInfo, schema_id: int):
        return DatabaseSchema.objects.get(id=schema_id)


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
