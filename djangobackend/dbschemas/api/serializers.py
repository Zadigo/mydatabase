from dbschemas.models import DatabaseSchema
from dbtables.api.serializers import DatabaseTableSerializer
from rest_framework import serializers


class DatabaseSchemaSerializer(serializers.ModelSerializer):
    tables = DatabaseTableSerializer(many=True, read_only=True, source='databasetable_set')

    class Meta:
        model = DatabaseSchema
        fields = '__all__'
