import type { SimpleTable } from '../../../app/composables/use/tables/index'
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
