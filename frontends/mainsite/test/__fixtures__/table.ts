import type { ColumnTypeOptions, SimpleTable, TableDocument } from '../../app/types'
import { faker } from '@faker-js/faker'

export const mockDataSource = {
  id: faker.number.int({ min: 1, max: 1000 }),
  firstname: faker.person.firstName(),
  lastname: faker.person.lastName(),
  email: faker.internet.email(),
  created_at: faker.date.past().toISOString(),
  updated_at: faker.date.recent().toISOString()
}

export const tableFixture: SimpleTable = {
  id: faker.number.int({ min: 1, max: 1000 }),
  name: faker.lorem.words(3),
  description: faker.lorem.sentence(),
  active_document_datasource: 'uuid-123-456',
  component: 'data-table',
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

export const staticTableDocumentFixture: TableDocument = {
  ...tableDocumentFixture,
  name: 'Test Document',
  document_uuid: 'uuid-123-456',
  column_names: ['id', 'name', 'email'],
  column_options: [
    {
      name: 'id',
      searchable: true,
      sortable: true,
      columnType: 'Number',
      editable: false,
      visible: true
    },
    {
      name: 'name',
      searchable: true,
      sortable: true,
      columnType: 'String',
      editable: true,
      visible: true
    },
    {
      name: 'email',
      searchable: true,
      sortable: true,
      columnType: 'String',
      editable: true,
      visible: true
    }
  ],
  column_types: [
    {
      name: 'id',
      columnType: 'Number'
    },
    {
      name: 'name',
      columnType: 'String'
    },
    {
      name: 'email',
      columnType: 'String'
    }
  ],
  column_type_options: [
    { name: 'id', newName: 'id', columnType: 'Number', unique: true, nullable: false, visible: true },
    { name: 'name', newName: 'name', columnType: 'String', unique: false, nullable: false, visible: true },
    { name: 'email', newName: 'email', columnType: 'String', unique: true, nullable: false, visible: true }
  ]
}

export const columnTypeOptionsFixture: ColumnTypeOptions = {
  name: faker.lorem.word(),
  newName: faker.lorem.word(),
  columnType: 'String',
  unique: faker.datatype.boolean(),
  nullable: faker.datatype.boolean(),
  visible: faker.datatype.boolean()
}
