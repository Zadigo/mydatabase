import type { Database } from '../../app/types'
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
