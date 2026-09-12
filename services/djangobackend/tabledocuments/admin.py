from django.contrib import admin
from django.contrib.messages import SUCCESS, add_message

from tabledocuments.django_tasks import (
    create_csv_from_url,
    huey_task,
    update_document_options,
)
from tabledocuments.models import TableDocument


@admin.register(TableDocument)
class TableDocumentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'file', 'created_at', 'updated_at')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_per_page = 25
    actions = ('update_document_options', 'refresh_document')

    def update_document_options(self, request, queryset):
        for document in queryset:
            if document.file is not None:
                update_document_options.s(
                    kwargs={
                        'document_uuid': str(document.document_uuid), 
                        'from_file': True
                    },
                    countdown=3
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
                task = create_csv_from_url.s(document.url)
                huey_task.enqueue(task)
