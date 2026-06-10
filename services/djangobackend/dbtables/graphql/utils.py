from graphene_django import DjangoObjectType
from graphql import GraphQLResolveInfo
from dbtables.models import DatabaseTable
from django.db.models import QuerySet


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
    def get_queryset(cls, queryset: QuerySet[DatabaseTable], info: GraphQLResolveInfo):
        prefetched = queryset.prefetch_related('documents')
        selected = prefetched.select_related('database_schema')
        qs = selected.all()

        # if info.context.user.is_anonymous:
        #     return qs.none()
        
        # qs = qs.filter(database_schema__user=info.context.user)
        return qs
