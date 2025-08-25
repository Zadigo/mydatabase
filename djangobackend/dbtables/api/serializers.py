from dbtables.models import DatabaseTable
from rest_framework import serializers


class DatabaseTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatabaseTable
        exclude = ['database_schema', 'documents']
