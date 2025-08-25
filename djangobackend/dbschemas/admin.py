from dbschemas.models import DatabaseSchema
from django.contrib import admin


@admin.register(DatabaseSchema)
class DatabaseSchemaAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']
    search_fields = ['name']
    ordering = ['-created_at']
