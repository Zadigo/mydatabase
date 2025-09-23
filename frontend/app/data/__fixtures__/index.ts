import type { Database } from '~/types'

export { endpointsFixture } from './endpoints'

export const databaseFixture: Database = {
  id: 1,
  name: 'Test Database',
  updated_at: '2024-01-01T00:00:00Z',
  created_at: '2024-01-01T00:00:00Z',
  tables: [
    {
      id: 1,
      name: 'Test Collection',
      description: 'A simple table description',
      component: 'data-table',
      active: true,
      active_document_datasource: '123e4567-e89b-12d3-a456-426614174000',
      updated_at: '2024-01-01T00:00:00Z',
      created_at: '2024-01-01T00:00:00Z',
      documents: [
        {
          id: 1,
          document_uuid: '123e4567-e89b-12d3-a456-426614174000',
          name: 'Simple data',
          updated_at: '2024-01-01T00:00:00Z',
          created_at: '2024-01-01T00:00:00Z',
          column_names: ['id', 'title', 'content'],
          column_types: [
            {
              name: 'id',
              columnType: 'String',
              unique: false,
              nullable: false
            },
            {
              name: 'title',
              columnType: 'String',
              unique: false, 
              nullable: false
            },
            {
              name: 'content',
              columnType: 'String',
              unique: false,
              nullable: true
            }
          ],
          column_options: [
            {
              name: 'id',
              searchable: true,
              sortable: true,
              editable: true,
              visible: true
            },
            {
              name: 'title',
              searchable: true,
              sortable: true,
              editable: true,
              visible: true
            },
            {
              name: 'content',
              searchable: true,
              sortable: true,
              editable: true,
              visible: true
            }
          ]
        }
      ]
    }
  ]
}

export const databasesFixture: Database[] = [databaseFixture]
