import graphene
from graphene_django import DjangoObjectType, DjangoListField

from dbtables.models import DatabaseTable

class DatabaseTableType(DjangoObjectType):
    class Meta:
        model = DatabaseTable
        fields = [
            'id',
            'name',
            'description',
            'database_schema',
            'active_document_datasource',
            'documents',
            'component',
            'slug',
            'active',
            'updated_at',
            'created_at'
        ]

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.prefetch_related('documents').select_related('database_schema').all()



class DatabaseTableQuery(graphene.ObjectType):
    all_database_tables = DjangoListField(DatabaseTableType)
    table_by_id = graphene.Field(DatabaseTableType, table_id=graphene.String(required=True))
    search_tables = DjangoListField(
        DatabaseTableType,
        name=graphene.String(required=False),
        # description=graphene.String(required=False),
        database_schema=graphene.String(required=False),
        document_name=graphene.String(required=False),
        active=graphene.Boolean(required=False)
    )

    def resolve_all_database_tables(root, info):
        return DatabaseTable.objects.all()

    def resolve_table_by_id(root, info, table_id: str):
        return DatabaseTable.objects.get(id=table_id)

    def resolve_search_tables(root, info, **kwargs):
        name = kwargs.get('name')
        qs = DatabaseTable.objects.all()
        
        if name is None:
            return qs
        
        qs = qs.filter(name__icontains=name)

        description = kwargs.get('description')
        if description is not None:
            qs = qs.filter(description__icontains=description)

        database_schema = kwargs.get('database_schema')
        if database_schema is not None:
            qs = qs.filter(database_schema__name__icontains=database_schema)

        document_name = kwargs.get('document_name')
        if document_name is not None:
            qs = qs.filter(document_name__name__icontains=document_name)

        active = kwargs.get('active', True)
        return qs.filter(active=active)


