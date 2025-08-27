from django.contrib import admin

from dbtables.models import DatabaseTable


@admin.register(DatabaseTable)
class DatabaseTableAdmin(admin.ModelAdmin):
    list_display = ['name', 'database_schema', 'created_at', 'updated_at']
    search_fields = ['name', 'description']
    ordering = ['-created_at']
