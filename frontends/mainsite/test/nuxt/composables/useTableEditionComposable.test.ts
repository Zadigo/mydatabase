import { describe, it, expect, vi, beforeEach } from 'vitest'
import type { Database, SimpleTable } from '~/types'
import { databaseFixture, tableFixture, staticTableDocumentFixture } from '~~/test/__fixtures__'

const table: SimpleTable = {
  ...tableFixture,
  documents: [
    staticTableDocumentFixture
  ]
}

const db: Database = {
  ...databaseFixture,
  tables: [
    table
  ],
}

const { mockedUseDatabases } = vi.hoisted(() => {
  const fn = vi.fn<typeof import('~/composables/use/databases')._useDatabases>(() => ({
    allTableDocuments: computed(() => [staticTableDocumentFixture]),
    currentDatabase: computed(() => db),
    availableTableNames: computed(() => [ 'Test Table' ]),
    availableTables: computed(() => [ table ]),
    databases: computed(() => [ db ]),
    hasTables: computed(() => true),
    routeId: { databaseId: '1' },
    search: computed(() => ''),
    searched: computed(() => [ db ])
  }))

  return {
    mockedUseDatabases: fn
  }
})

vi.mock('~/composables/use/databases' , async (original) => {
  const actual = await original<typeof import('~/composables/use/databases')>()

  return {
    ...actual,
    _useDatabases: mockedUseDatabases
  }
})

describe('useTableEditionComposable', () => {
  beforeEach(() => {
    vi.resetModules()
  })

  it('should return default properties', async () => {
    const { useTableEditionComposable } = await import('~/composables/use/tables/edition')
    
    const defaults = useTableEditionComposable()
    
    expect(defaults).toHaveProperty('selectedTableName')
    expect(defaults).toHaveProperty('selectedTable')
    expect(defaults).toHaveProperty('selectedTableDocumentName')
    expect(defaults).toHaveProperty('tableDocuments')
    expect(defaults).toHaveProperty('hasDocuments')
    expect(defaults).toHaveProperty('selectedTableDocument')
    expect(defaults).toHaveProperty('selectedTableDocumentNames')
    
    expect(defaults.selectedTableName.value).toBeUndefined()
    expect(defaults.selectedTableDocumentName.value).toBeUndefined()
  })
  
  it('should select by table name', async () => {
    mockedUseDatabases.mockReturnValueOnce({
      allTableDocuments: computed(() => db.tables[0]?.documents || []),
      currentDatabase: computed(() => db),
      availableTableNames: computed(() => ['Test Table']),
      availableTables: computed(() => db.tables),
      databases: computed(() => [db]),
      hasTables: computed(() => true),
      routeId: { databaseId: db.id.toString() },
      search: computed(() => ''),
      searched: computed(() => [db])
    })

    const { useTableEditionComposable } = await import('~/composables/use/tables/edition')
    
    const defaults = useTableEditionComposable()
    defaults.selectedTable.value = tableFixture

    expect(toValue(defaults.hasData)).toBe(false)
    expect(toValue(defaults.selectedTableDocumentNames)).toEqual(['Test Document'])
    expect(toValue(defaults.hasDocuments)).toBe(true)
  })

  it('should select table active datasource when set', async () => {
    const table = db.tables[0]
    
    if (table) {
      table.active_document_datasource = staticTableDocumentFixture.document_uuid
    }

    mockedUseDatabases.mockReturnValueOnce({
      allTableDocuments: computed(() => db.tables[ 0 ]?.documents || []),
      currentDatabase: computed(() => db),
      availableTableNames: computed(() => [ 'Test Table' ]),
      availableTables: computed(() => db.tables),
      databases: computed(() => [ db ]),
      hasTables: computed(() => true),
      routeId: { databaseId: db.id.toString() },
      search: computed(() => ''),
      searched: computed(() => [ db ])
    })

    const { useTableEditionComposable } = await import('~/composables/use/tables/edition')

    const defaults = useTableEditionComposable()
    defaults.selectedTable.value = tableFixture

    expect(toValue(defaults.))
  })
})
