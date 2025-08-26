from rest_framework import serializers
from tabledocuments.models import TableDocument


class SimpleDocumentSerializer(serializers.ModelSerializer):
    """A serializer that returns the document details *without*
    the data it contains. It returns only metadata about the document."""
    
    class Meta:
        model = TableDocument
        fields = ['id', 'document_uuid', 'name', 'updated_at', 'created_at']
