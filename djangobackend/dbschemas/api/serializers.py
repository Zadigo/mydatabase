from dbschemas.models import DatabaseSchema, DatabaseTable
from rest_framework import serializers


class DatabaseTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatabaseTable
        fields = '__all__'
        exclude = ['database_schema', 'documents']


class DatabaseSchemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatabaseSchema
        fields = '__all__'
