from typing import Optional

from asgiref.sync import async_to_sync
from django.db.models import Q
from mcp.types import TextContent
from mcp_server import MCPToolset, ModelQueryToolset
from tabledocuments.api.serializer import SimpleDocumentSerializer
from tabledocuments.logic.edit import DocumentEdition
from tabledocuments.models import TableDocument


class TableDocumentsQueryTool(ModelQueryToolset):
    model = TableDocument
    search_fields = [
        'name',
        'file',
        'column_names',
        'column_options',
        'column_types',
        'url',
        'google_sheet_id',
        'updated_at',
        'created_at'
    ]


class TableDocumentsTools(MCPToolset):
    def get_document(self, document_uuid: str, name: Optional[str] = None) -> dict:
        """Returns the details of a document file (TableDocument)

        Args:
            document_uuid: The UUID of the document to retrieve.
            name: Optional name of the document to retrieve. If provided, it will be used as an additional filter.

        Returns:
            A dictionary containing the document details, or None if the document does not exist.
        """
        try:
            document = TableDocument.objects.get(
                Q(document_uuid=document_uuid) |
                Q(name=name)
            )
        except TableDocument.DoesNotExist:
            return {}

        return SimpleDocumentSerializer(document).data

    def get_document_content(self, document_id: str | int) -> dict:
        """Return the content of a document as text. This is used to retrieve 
        the content of a document for editing or display purposes.
        
        Args:
            document_id: The ID of the document to retrieve.

        Returns:
            A dictionary containing the document content as text, or an empty dictionary if the document does not exist.
        """
        instance = DocumentEdition()
        state, document = async_to_sync(instance.load_document_by_id)(document_id)

        if document is None:
            return {}
        
        content = document.content.to_csv()
        return TextContent(type='text', text=content)
