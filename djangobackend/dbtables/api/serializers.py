from dbtables.models import DatabaseTable
from rest_framework import serializers
from tabledocuments.api.serializer import SimpleDocumentSerializer


class DatabaseTableSerializer(serializers.ModelSerializer):
    documents = SimpleDocumentSerializer(
        many=True, read_only=True, source='tabledocument_set')

    class Meta:
        model = DatabaseTable
        exclude = ['database_schema']
