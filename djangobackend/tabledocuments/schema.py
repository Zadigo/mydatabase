from graphene import Boolean, Field, Mutation, ObjectType, String
from graphql.type import GraphQLResolveInfo
from graphene.types.generic import GenericScalar
from graphene_django import DjangoObjectType
from graphene_django.fields import DjangoListField

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



# class MutateColumnOption(ObjectType):
#     class Arguments:
#         new_name = String(required=False)
#         column_type = String(required=False)
#         unique = Boolean(required=False)
#         visible = Boolean(required=False)
#         nullable = Boolean(required=False)

#     column_option = Field(ColumnOptionType)

#     @classmethod
#     def mutate(cls, root, info: GraphQLResolveInfo, **params):
#         document_uuid = params.pop('document_uuid')

#         validated_options = ColumnOption(**params)
#         document = TableDocument.objects.get(document_uuid=document_uuid)

#         selected_option = list(
#             filter(
#                 lambda x: x['name'] == validated_options.name,
#                 document.column_options
#             )
#         )

#         for key, value in validated_options.model_dump().items():
#             if value is not None:
#                 document[key] = value

#         document.save()
#         return cls(column_option=validated_options)


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
