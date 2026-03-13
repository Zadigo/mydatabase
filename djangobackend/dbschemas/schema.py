import graphene
from graphene_django.types import DjangoObjectType
from graphene_django.fields import DjangoListField
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
    def get_queryset(cls, queryset, info):
        return queryset.prefetch_related('database_schema').all()


class DbSchemaQuery(graphene.ObjectType):
    all_dbschemas = DjangoListField(DatabaseSchemaType, name=graphene.String(required=False))
    db_schema_by_id = graphene.Field(DatabaseSchemaType, schema_id=graphene.Int(required=True))

    def resolve_all_dbschemas(root, info, name: str = None):
        qs = DatabaseSchema.objects.all()
        if name is not None:
            return qs.filter(name__icontains=name)
        return qs


class DatabaseProviderQuery(graphene.ObjectType):
    all_providers = DjangoListField(DatabaseProviderType)
    provider_by_id = graphene.Field(DatabaseProviderType, schema_id=graphene.String(required=True))

    def resolve_all_providers(root, info):
        return DatabaseProvider.objects.all()
    
    def resolve_provider_by_id(root, info, schema_id: str):
        return DatabaseProvider.objects.get(database_schema__id=schema_id)


class CreateDatabaseMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    db_schema = graphene.Field(DatabaseSchemaType)

    @classmethod
    def mutate(cls, root, info, name: str):
        instance = DatabaseSchema.objects.create(name=name)
        return CreateDatabaseMutation(db_schema=instance)

    # @classmethod
    # def mutate(cls, root, info, text, id):
    #     question = Question.objects.get(pk=id)
    #     question.text = text
    #     question.save()
    #     # Notice we return an instance of this mutation
    #     return QuestionMutation(question=question)
