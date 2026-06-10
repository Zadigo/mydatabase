import graphene
from graphene_django import DjangoListField
from graphql import GraphQLResolveInfo

from dbtables.models import DatabaseTable
from dbtables.graphql.utils import DatabaseTableType

class DatabaseTableQuery(graphene.ObjectType):
    all_database_tables = DjangoListField(
        DatabaseTableType,
    )
    table_by_id = graphene.Field(
        DatabaseTableType, 
        table_id=graphene.String(required=True)
    )
    search_tables = DjangoListField(
        DatabaseTableType,
        name=graphene.String(required=False),
        schema_name=graphene.String(required=False),
        document_name=graphene.String(required=False),
        has_file=graphene.Boolean(required=False),
        active=graphene.Boolean(required=False)
    )

    def resolve_all_database_tables(root, info: GraphQLResolveInfo):
        return DatabaseTable.objects.all()

    def resolve_search_tables(root, info: GraphQLResolveInfo, **kwargs):
        qs = DatabaseTable.objects.all()
        
        name = kwargs.get('name')
        if name is not None:        
            qs = qs.filter(name__icontains=name)

        description = kwargs.get('description')
        if description is not None:
            qs = qs.filter(description__icontains=description)

        schema_name = kwargs.get('schema_name')
        if schema_name is not None:
            qs = qs.filter(database_schema__name__icontains=schema_name)

        document_name = kwargs.get('document_name')
        if document_name is not None:
            qs = qs.filter(documents__name__icontains=document_name)

        has_file = kwargs.get('has_file')
        if has_file is not None:
            qs = qs.filter(documents__isnull=has_file)
    
        active = kwargs.get('active', True)
        print(kwargs)
        return qs.filter(active=active)

    def resolve_table_by_id(root, info: GraphQLResolveInfo, table_id: str):
        return DatabaseTable.objects.get(id=table_id)
