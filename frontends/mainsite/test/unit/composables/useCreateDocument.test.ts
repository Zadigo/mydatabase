import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useCreateDocument } from '../../../app/composables/use/documents/edition'

describe('useCreateDocument', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('should initialize with default params', () => {
    const result = useCreateDocument()
    expect(result).toBeDefined()
    expect(result.newDocument.value).toEqual({
      name: '',
      url: '',
      google_sheet_id: '',
      file: null,
      entry_key: null,
      using_columns: []
    })
  })
})
