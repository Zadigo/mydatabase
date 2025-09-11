from rest_framework import serializers
from endpoints.models import PublicApiEndpoint


class SimpleTableSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()


class SimpleDatabaseSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    tables = SimpleTableSerializer(
        many=True, read_only=True, source='databasetable_set')


class PublicApiEndpointSerializer(serializers.ModelSerializer):
    database_schema = SimpleDatabaseSerializer(read_only=True)

    class Meta:
        model = PublicApiEndpoint
        read_only_fields = ['id']
        fields = [
            'id', 'methods', 'endpoint',
            'endpoint_uuid', 'database_schema'
        ]
