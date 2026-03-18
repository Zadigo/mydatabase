import graphene
from graphene_django.types import DjangoObjectType
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
