from django.contrib import admin
from endpoints.models import PublicApiEndpoint, SecretApiEndpoint


@admin.register(PublicApiEndpoint)
class PublicApiEndpointAdmin(admin.ModelAdmin):
    list_display = ['endpoint_uuid', 'endpoint',
                    'public_key', 'bearer_token', 'methods', 'created_at']
    readonly_fields = ['endpoint_uuid',
                       'public_key', 'bearer_token', 'created_at']
    search_fields = ['endpoint', 'public_key', 'bearer_token']
    list_filter = ['created_at', 'methods']


@admin.register(SecretApiEndpoint)
class SecretApiEndpointAdmin(admin.ModelAdmin):
    list_display = ['endpoint_uuid', 'endpoint', 'secret_key', 'created_at']
    readonly_fields = ['endpoint_uuid', 'secret_key', 'created_at']
    search_fields = ['endpoint', 'secret_key']
    list_filter = ['created_at']
