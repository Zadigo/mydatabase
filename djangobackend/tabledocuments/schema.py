from graphene import Boolean, Field, ObjectType, String
from graphql.type import GraphQLResolveInfo
from graphene.types.generic import GenericScalar
from graphene_django import DjangoObjectType
from graphene_django.fields import DjangoListField

from tabledocuments.models import TableDocument


class ColumnOptionType(ObjectType):
    name = String()
    newName = String()
    columnType = String()
    unique = Boolean()
    visible = Boolean()
    nullable = Boolean()


class TableDocumentsType(DjangoObjectType):
    column_options = GenericScalar()
    column_types = GenericScalar()
    # mixed_options = GenericScalar()

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

    def resolve_column_options(root, info: GraphQLResolveInfo):
        return root.column_options or []

    def resolve_column_types(root, info: GraphQLResolveInfo):
        return root.column_types or {}

    # def resolve_mixed_options(root, info: GraphQLResolveInfo):
    #     return root.mixed_options or []


class TableDocumentsQuery(ObjectType):
    all_documents = DjangoListField(TableDocumentsType, name = String(required=False))
    document_by_id = Field(TableDocumentsType, document_uuid = String(required=True))
    get_column_option = Field(
        ColumnOptionType, 
        document_uuid=String(required=True), 
        column_name=String(required=True)
    )

    def resolve_all_documents(root, info: GraphQLResolveInfo, name: str = None):
        qs = TableDocument.objects.all()
        if name is not None:
            return qs.filter(name__icontains=name)
        return qs

    def resolve_document_by_id(root, info, document_uuid: str):
        return TableDocument.objects.get(document_uuid=document_uuid)

    def resolve_get_column_option(root, info, document_uuid: str, column_name: str):
        document = TableDocument.objects.get(document_uuid=document_uuid)
        column = list(filter(lambda x: x['name'] == column_name, document.column_options))

        try:
            return column[-0]
        except:
            return {}

