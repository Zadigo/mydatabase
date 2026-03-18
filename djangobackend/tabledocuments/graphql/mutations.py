from graphene import Field, Mutation, String
from graphql.type import GraphQLResolveInfo
from graphene.types.generic import GenericScalar

from tabledocuments.models import TableDocument
from tabledocuments.graphql.utils import TableDocumentsType



class MutateTableDocument(Mutation):
    class Arguments:
        document_uuid = String(required=True)
        name = String(required=False)
        column_type_options = GenericScalar(required=False)

    tableDocument = Field(TableDocumentsType)

    @classmethod
    def mutate(cls, root, info: GraphQLResolveInfo, **params):
        document_uuid = params.pop('document_uuid')
        document = TableDocument.objects.get(document_uuid=document_uuid)

        for key, value in params.items():
            if value is not None:
                setattr(document, key, value)

        document.save()
        return cls(tableDocument=document)
