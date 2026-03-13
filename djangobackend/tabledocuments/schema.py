
from graphene import Field, ObjectType, String
from graphql.type import GraphQLResolveInfo
from graphene.types import List
from graphene_django import DjangoObjectType
from graphene_django.fields import DjangoListField

from tabledocuments.models import TableDocument


class TableDocumentsType(DjangoObjectType):
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


class TableDocumentsQuery(ObjectType):
    all_documents = DjangoListField(TableDocumentsType, name = String(required=False))
    document_by_id = Field(TableDocumentsType, document_uuid = String(required=True))

    def resolve_all_documents(root, info: GraphQLResolveInfo, name: str = None):
        qs = TableDocument.objects.all()
        if name is not None:
            return qs.filter(name__icontains=name)
        return qs

    def resolve_document_by_id(root, info, document_uuid: str):
        return TableDocument.objects.get(document_uuid=document_uuid)
