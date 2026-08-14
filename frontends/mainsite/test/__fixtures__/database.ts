import type { Database, DatabaseFunction, SimpleTable } from '../../app/types'
import { faker } from '@faker-js/faker'

export const databaseFixture: Database = {
  id: 1,
  name: 'Test Database',
  tables: [],
  active: true,
  paused: false,
  database_functions: null,
  database_triggers: null,
  document_relationships: null,
  slug: 'test-database',
  updated_at: new Date().toISOString(),
  created_at: new Date().toISOString()
}

export const databaseStaticFixture: Database = {
  ...databaseFixture,
  id: 1
}

export const datatabaseFunctionFixture: DatabaseFunction = {
  function: {
    name: 'Test Function',
    table: 'test_table',
    columns: [],
    returns: {
      type: 'void',
      value: ''
    },
    chain_to: [],
    signals: {
      failure: {
        do: 'Skip',
        default_value: ''
      }
    }
  }
}

export const tableFixture: SimpleTable = {
  id: 1,
  name: 'Test Table',
  description: 'This is a test table',
  active_document_datasource: null,
  component: 'data-table',
  active: true,
  documents: [],
  updated_at: new Date().toISOString(),
  created_at: new Date().toISOString()
}
