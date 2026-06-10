from graphene import Boolean, Field, ObjectType, String
from graphql.type import GraphQLResolveInfo
from graphene_django.fields import DjangoListField

from tabledocuments.models import TableDocument
from tabledocuments.graphql.utils import TableDocumentsType


class ColumnOptionType(ObjectType):
    name = String()
    newName = String()
    columnType = String()
    unique = Boolean()
    visible = Boolean()
    nullable = Boolean()


class TableDocumentsQuery(ObjectType):
    all_documents = DjangoListField(
        TableDocumentsType, 
        name = String(required=False)
    )
    document_by_id = Field(
        TableDocumentsType,
        document_uuid = String(required=True)
    )
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

    def resolve_document_by_id(root, info: GraphQLResolveInfo, document_uuid: str):
        return TableDocument.objects.get(document_uuid=document_uuid)

    def resolve_get_column_option(root, info: GraphQLResolveInfo, document_uuid: str, column_name: str):
        document = TableDocument.objects.get(document_uuid=document_uuid)

        if column_name not in document.column_names:
            return {}

        column = list(filter(lambda x: x['name'] == column_name, document.column_options))

        try:
            return column[-1]
        except:
            return {}
