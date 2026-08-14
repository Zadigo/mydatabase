import { describe, it, expect, beforeEach } from 'vitest'
import { useEditDocument } from '~/composables/use/documents/edition'
import { createPinia, setActivePinia } from 'pinia'

describe('useEditDocument', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('should initialize with default params', () => {
    const result = useEditDocument()
    expect(result).toBeDefined()
  })
})
