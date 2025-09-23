from django.contrib import admin
from django.contrib.messages import SUCCESS, add_message
from tabledocuments.models import TableDocument
from tabledocuments.tasks import (create_csv_file_from_data,
                                  get_document_from_url,
                                  update_document_options)


@admin.register(TableDocument)
class TableDocumentsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'file', 'created_at', 'updated_at']
    list_display_links = ['id', 'name']
    search_fields = ['name']
    list_per_page = 25
    actions = ['update_document_options', 'refresh_document']

    def update_document_options(self, request, queryset):
        for document in queryset:
            if document.file is not None:
                update_document_options.apply_async(
                    args=[str(document.document_uuid), document.file.path],
                    countdown=10
                )

        add_message(
            request,
            SUCCESS,
            f"Started update for {queryset.count()} documents."
        )

    def refresh_document(self, request, queryset):
        for document in queryset:
            if document.file is not None:
                document.file.delete()
                document.file = None
                document.column_names = []
                document.column_types = {}
                document.column_options = {}
                document.save()

            if document.url:
                get_document_from_url.apply_async(
                    args=[document.url],
                    countdown=10,
                    link=[create_csv_file_from_data.s(document.id, 'results')]
                )
