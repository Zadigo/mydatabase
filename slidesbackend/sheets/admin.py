from django.contrib import admin

from sheets.models import Sheet, Webhook


@admin.register(Sheet)
class SheetAdmin(admin.ModelAdmin):
    list_display = ['sheet_id', 'name', 'created_on']
    readonly_fields = ['sheet_id']
    fieldsets = [
        [
            None, 
            {
                'fields': ['user', 'name', 'sheet_id']
            }
        ],
        [
            'Google sheet', 
            {
                'fields': ['url']
            }
        ],
        [
            'Sources', 
            {
                'fields': ['csv_file', 'endpoint_url', 'endpoint_data_key']
            }
        ],
        [
            'Columns', 
            {
                'fields': ['columns', 'column_types']
            }
        ]
    ]


@admin.register(Webhook)
class WebhookAdmin(admin.ModelAdmin):
    list_display = ['webhook_id']
    readonly_fields = ['webhook_id']
