from graphql.type import GraphQLResolveInfo
from graphene.types.generic import GenericScalar
from graphene_django import DjangoObjectType

from tabledocuments.models import TableDocument
from django.db.models import QuerySet

class TableDocumentsType(DjangoObjectType):
    column_options = GenericScalar()
    column_types = GenericScalar()

    class Meta:
        model = TableDocument
        fields = [
            'document_uuid',
            'name',
            'column_names',
            'column_options',
            'column_types',
            'url',
            'google_sheet_id',
            'updated_at',
            'created_at'
        ]
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'file': ['isna'],
            'updated_at': ['gt', 'gte', 'lt', 'lte']
        }

    @classmethod
    def get_queryset(cls, queryset: QuerySet[TableDocument], info: GraphQLResolveInfo):
        # if info.context.user.is_anonymous:
        #     return queryset.none()
        # return queryset.filter(user=info.context.user)
        return queryset.all()

    def resolve_column_options(root, info: GraphQLResolveInfo):
        return root.column_options or []

    def resolve_column_types(root, info: GraphQLResolveInfo):
        return root.column_types or {}
