from dbschemas.models import DatabaseSchema, DatabaseProvider
from django.contrib import admin


@admin.register(DatabaseSchema)
class DatabaseSchemaAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']
    search_fields = ['name']
    ordering = ['-created_at']


@admin.register(DatabaseProvider)
class DatabaseProviderAdmin(admin.ModelAdmin):
    list_display = ['id', 'database_schema', 'created_at']
    search_fields = ['database_schema__name']
    ordering = ['-created_at']
