import type { Database } from '~/types'

export const databaseFixture: Database = {
  id: 1,
  name: 'Test Database',
  tables: [
    {
      id: 1,
      name: 'Test Collection',
      documents: [
        {
          id: 1,
          data: [
            {
              title: 'Test Document',
              content: 'This is a test document.'
            }
          ]
        }
      ]
    }
  ]
}

export const databasesFixture: Database[] = [databaseFixture]
