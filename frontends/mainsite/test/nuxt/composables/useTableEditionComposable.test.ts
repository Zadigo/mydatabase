import { describe, it, expect, vi } from 'vitest'
import { useTableEditionComposable  } from '~/composables/use/tables/edition'
import type { Database, SimpleTable } from '~/types'
import { databaseFixture, tableFixture } from '~~/test/__fixtures__'

const _useDatabases = vi.fn(() => {
  const table: SimpleTable = {
    ...tableFixture,
    documents: []
  }

  const db: Database = {
    ...databaseFixture,
    tables: [
      table
    ],
  }

  return {
    currentDatabase: ref([ db ])
  }
})

vi.mock('~/composables/use/databases' , async (original) => {
  const actual = await original<typeof import('~/composables/use/databases')>()

  return {
    ...actual,
    _useDatabases: vi.fn(() => {
      const table: SimpleTable = {
        ...tableFixture,
        documents: []
      }

      const db: Database = {
        ...databaseFixture,
        tables: [
          table
        ],
      }

      return {
        currentDatabase: ref([db])
      }
    })
  }
})

describe('useTableEditionComposable', () => {
  it('should return default properties', () => {
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
})
