from dbschemas.models import DatabaseSchema, DatabaseTable
from django.contrib import admin


@admin.register(DatabaseSchema)
class DatabaseSchemaAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']
    search_fields = ['name']
    ordering = ['-created_at']


@admin.register(DatabaseTable)
class DatabaseTableAdmin(admin.ModelAdmin):
    list_display = ['name', 'database_schema', 'created_at', 'updated_at']
    search_fields = ['name', 'database_schema__name']
    ordering = ['-created_at']
