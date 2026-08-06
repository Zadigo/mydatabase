import type { SimpleTable, TableDocument } from '../../app/types'
import { faker } from '@faker-js/faker' 

export const tableFixture: SimpleTable = {
  id: faker.number.int({ min: 1, max: 1000 }),
  name: faker.lorem.words(3),
  description: faker.lorem.sentence(),
  active_document_datasource: faker.lorem.word(),
  component: 'table',
  active: faker.datatype.boolean(),
  documents: [],
  created_at: faker.date.past().toISOString(),
  updated_at: faker.date.recent().toISOString()
}

export const tableDocumentFixture: TableDocument = {
  id: faker.number.int({ min: 1, max: 1000 }),
  name: faker.lorem.words(3),
  document_uuid: faker.string.uuid(),
  column_names: [faker.lorem.word(), faker.lorem.word(), faker.lorem.word()],
  column_options: [],
  column_types: [],
  column_type_options: [],
  created_at: faker.date.past().toISOString(),
  updated_at: faker.date.recent().toISOString()
}
