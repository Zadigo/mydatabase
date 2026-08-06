import type { Database, DatabaseFunction } from '../../app/types'
import { faker } from '@faker-js/faker'

export const databaseFixture: Database = {
  id: faker.number.int({ min: 1, max: 1000 }),
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
