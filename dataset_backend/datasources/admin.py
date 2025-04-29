import pandas
from django.contrib import admin
from datasources.utils import create_column_data_types
from datasources.models import DataSource, Webhook
from django.contrib import messages


@admin.register(DataSource)
class DataSourceAdmin(admin.ModelAdmin):
    list_display = ['data_source_id', 'name', 'created_on']
    readonly_fields = ['data_source_id']
    fieldsets = [
        [None, {'fields': ['user', 'name', 'data_source_id']}],
        ['Sources', {'fields': ['google_sheet_url',
                                'csv_file', 'endpoint_url', 'endpoint_data_key']}],
        ['Columns', {'fields': ['columns']}]
    ]
    # actions = ['reload_columns']

    # def reload_columns(self, request, queryset):
    #     for data_source in queryset:
    #         df = pandas.read_csv(data_source.csv_file.path)
    #         data_source.columns = create_column_data_types(df.columns)
    #         data_source.save()
    #     message = f'Updated {queryset.count()} data sources'
    #     messages.add_message(request, messages.SUCCESS, message)


@admin.register(Webhook)
class WebhookAdmin(admin.ModelAdmin):
    list_display = ['webhook_id']
    readonly_fields = ['webhook_id']
