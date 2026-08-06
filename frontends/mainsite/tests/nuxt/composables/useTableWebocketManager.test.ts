import { describe, it, expect, vi } from 'vitest'
import { useTableWebocketManager } from '~/composables'
import { tableDocumentFixture, tableFixture  } from '../../__fixtures__'

describe('useTableWebocketManager', () => {
  it('should initialize with default params', () => {
    const table = ref(tableFixture)
    const tableDocument = ref(tableDocumentFixture)
    const result = useTableWebocketManager(table, tableDocument)
    expect(result).toBeDefined()
  })
})
