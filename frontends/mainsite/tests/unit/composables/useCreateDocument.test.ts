import { describe, it, expect } from 'vitest'
import { useCreateDocument } from '../../../app/composables/use/documents/edition'

describe.only('useCreateDocument', () => {
  it('should initialize with default params', () => {
    const result = useCreateDocument()
    expect(result).toBeDefined()

  })
})
