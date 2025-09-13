import uuid

from dbschemas.models import DatabaseSchema
from dbschemas.tasks import prefetch_relationships
from dbtables.api.serializers import DatabaseTableSerializer
from django.db.models import Q
from dbschemas.models import DatabaseProvider
from rest_framework import serializers


class DatabaseSchemaSerializer(serializers.ModelSerializer):
    tables = DatabaseTableSerializer(
        many=True, read_only=True, source='databasetable_set')

    class Meta:
        model = DatabaseSchema
        fields = '__all__'


class _FieldDefinition(serializers.Serializer):
    left = serializers.CharField()
    right = serializers.CharField()


class RelationshipSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    relationship_uuid = serializers.CharField(required=False)
    from_table = serializers.CharField()
    to_table = serializers.CharField()
    field_definitions = _FieldDefinition()
    meta_definitions = serializers.CharField(default='1-1')

    def validate(self, data):
        data['relationship_uuid'] = 'rel-' + str(uuid.uuid4())
        return data

    def validate_meta_definitions(self, value):
        allowed = ['1-1', 'm-m']
        if value not in allowed:
            raise serializers.ValidationError(
                f'Meta definition must be one of {allowed}')
        return value

    def create(self, validated_data):
        request = self._context['request']
        database_id = request.parser_context['kwargs']['pk']

        try:
            instance = DatabaseSchema.objects.get(id=database_id)
        except:
            raise serializers.ValidationError(detail={
                'database': 'Database with this id does not exist'
            })
        else:
            # Check that the documents that the tables that we are
            # trying to link to exist in this database
            tables = instance.databasetable_set.all()

            try:
                from_table = validated_data['from_table']
                table1 = tables.get(Q(id=from_table) | Q(slug=from_table))
            except Exception as e:
                print(e)
                raise serializers.ValidationError(detail={
                    'from_table': 'Table with this name does not exist in this database'
                })

            try:
                to_table = validated_data['to_table']
                table2 = tables.get(Q(id=to_table) | Q(slug=to_table))
            except Exception as e:
                print(e)
                raise serializers.ValidationError(detail={
                    'to_table': 'Table with this name does not exist in this database'
                })

            # Check that the relationship does not already exist
            for item in instance.document_relationships:
                if item['from_table'] == table1.slug and item['to_table'] == table2.slug:
                    raise serializers.ValidationError(detail={
                        'relationship': 'Relationship between these two tables already exists'
                    })

            # Create a name for this relationship This is for internal
            # use only so it does not need to be unique across the whole
            # database but for human identification purposes
            validated_data['name'] = table1.slug + '_to_' + table2.slug

            # Check that the columns does exist on the tables
            # that we are trying to link
            left_field = validated_data['field_definitions']['left']
            right_field = validated_data['field_definitions']['right']

            # If we do not have an active document datasource
            # we cannot create a relationship so just fail
            # gracefully
            if table1.active_document_datasource is None:
                return instance

            if table2.active_document_datasource is None:
                return instance

            table1_datasource = table1.documents.get(
                document_uuid=table1.active_document_datasource)
            table2_datasource = table2.documents.get(
                document_uuid=table2.active_document_datasource)

            message = 'Field "{field}" does not exist on the active document datasource for table "{table_name}"'

            if left_field not in table1_datasource.column_names:
                raise serializers.ValidationError(detail={
                    'field_definitions': {
                        'left': message.format(field=left_field, table_name=table1.name)
                    }
                })

            if right_field not in table2_datasource.column_names:
                raise serializers.ValidationError(detail={
                    'field_definitions': {
                        'right': message.format(field=right_field, table_name=table2.name)
                    }
                })

            instance.document_relationships.append(validated_data)
            instance.save()

            prefetch_relationships.apply_async(
                args=[instance.id], countdown=50)
        return instance


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
        fields = ['id', 'has_google_sheet_connection']
