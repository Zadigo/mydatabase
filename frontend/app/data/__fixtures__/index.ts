import type { Database } from '~/types'

export const databaseFixture: Database = {
  id: 1,
  name: 'Test Database',
  tables: [
    {
      id: 1,
      name: 'Test Collection',
      description: 'A simple table description',
      component: 'data-table',
      active: true,
      documents: [
        {
          id: 1,
          name: 'Simple data',
          data: [
            {
              id: 1,
              title: 'Test Document',
              content: 'This is a test document.'
            },
            {
              id: 2,
              title: 'Test Document 2',
              content: 'This is another test document.'
            }
          ]
        }
      ]
    }
  ]
}

export const databasesFixture: Database[] = [databaseFixture]
