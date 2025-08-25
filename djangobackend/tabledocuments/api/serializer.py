from rest_framework import serializers
from tabledocuments.models import TableDocument

class SimpleDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableDocument
        fields = ['id', 'name', 'updated_at', 'created_at']
