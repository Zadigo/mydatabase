import type { ColumnOptions, SimpleTable, TableDocument } from '#shared/types'
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
      visible: true,
      unique: true,
      nullable: false,
      newName: 'id'
    },
    {
      name: 'name',
      searchable: true,
      sortable: true,
      columnType: 'String',
      editable: true,
      visible: true,
      unique: false,
      nullable: false,
      newName: 'name'
    },
    {
      name: 'email',
      searchable: true,
      sortable: true,
      columnType: 'String',
      editable: true,
      visible: true,
      unique: true,
      nullable: false,
      newName: 'email'
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
  column_options: [
    { name: 'id', newName: 'id', columnType: 'Number', unique: true, nullable: false, visible: true, editable: false, searchable: true, sortable: true },
    { name: 'name', newName: 'name', columnType: 'String', unique: false, nullable: false, visible: true, editable: true, searchable: true, sortable: true },
    { name: 'email', newName: 'email', columnType: 'String', unique: true, nullable: false, visible: true, editable: true, searchable: true, sortable: true }
  ]
}

export const columnTypeOptionsFixture: ColumnOptions = {
  name: faker.lorem.word(),
  newName: faker.lorem.word(),
  columnType: 'String',
  unique: faker.datatype.boolean(),
  nullable: faker.datatype.boolean(),
  visible: faker.datatype.boolean()
}
