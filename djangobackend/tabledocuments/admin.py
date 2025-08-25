from django.contrib import admin
from tabledocuments.models import TableDocument

@admin.register(TableDocument)
class TableDocumentsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'file', 'created_at', 'updated_at']
    list_display_links = ['id', 'name']
    search_fields = ['name']
    list_per_page = 25
