import graphene
from graphene_django.types import DjangoObjectType
from graphene_django.fields import DjangoListField
from accounts.models import Organization, Profile
from django.contrib.auth import get_user_model

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        fields = [
            'first_name',
            'last_name',
            'email'
        ]
        filter_fields = {
            'first_name': ['exact']
        }


class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile
        fields = [
            'create_at',
            'updated_at'
        ]
        filter_fields = {}

    # @classmethod
    # def get_queryset(cls, queryset, info):
    #     return queryset.prefetch_related('user').all()


class OrganizationType(DjangoObjectType):
    class Meta:
        model = Organization
        fields = [
            'users',
            'name',
            'address',
            'created_at',
            'updated_at'
        ]
        filter_fields = {}

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.prefetch_related('users').all()


class AccountsQuery(graphene.ObjectType):
    all_users = DjangoListField(UserType)
    # all_profiles = DjangoListField(ProfileType)
    # all_organizations = DjangoListField(OrganizationType)

    # def resolve_all_users(root, info):
    #     return get_user_model().objects.all()
    
    # def resolve_all_profiles(root, info):
    #     return Profile.objects.all()

    # def resolve_all_organizations(root, info):
    #     return Organization.objects.all()
    
    
