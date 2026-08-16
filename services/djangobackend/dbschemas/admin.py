from django.contrib import admin

from dbschemas.models import DatabaseProvider, DatabaseSchema


@admin.register(DatabaseSchema)
class DatabaseSchemaAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    ordering = ('-created_at',)
    readonly_fields = ('slug',)


@admin.register(DatabaseProvider)
class DatabaseProviderAdmin(admin.ModelAdmin):
    list_display = ('id', 'database_schema', 'created_at')
    search_fields = ('database_schema__name',)
    ordering = ('-created_at',)
