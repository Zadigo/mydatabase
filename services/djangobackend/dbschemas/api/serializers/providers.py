
from rest_framework import serializers

from dbschemas.models import DatabaseProvider


class _ValidateGoogleSheet(serializers.Serializer):
    credentials = serializers.FileField(required=True)

    def validate_credentials(self, value):
        if not value.name.endswith('.json'):
            raise serializers.ValidationError(
                'Credentials file must be a JSON file')
        return value


class _ValidateAirtable(serializers.Serializer):
    airtable_base_id = serializers.CharField(required=True)
    airtable_table_name = serializers.CharField(required=True)
    airtable_api_key = serializers.CharField(required=True)


class ValidateIntegrationSerializer(serializers.Serializer):
    """Serializer used to validate credentials used to create
    integrations with external data providers like Airtable, 
    Google Sheets, etc."""

    airtable = _ValidateAirtable(required=False)
    google_sheets = _ValidateGoogleSheet(required=False)

    def create(self, validated_data):
        return None


class DatabaseProviderSerializer(serializers.ModelSerializer):
    has_google_sheet_connection = serializers.ReadOnlyField()

    class Meta:
        model = DatabaseProvider
        fields = ('id', 'has_google_sheet_connection')
