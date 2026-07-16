import { describe, it, expect } from 'vitest'
import { useEditDocument } from '../../../app/composables/use/documents/edition'
import { isRef } from 'vue'

describe.only('useEditDocument', () => {
  it('should initialize with default params', () => {
    const result = useEditDocument()
    expect(result).toBeDefined()
    expect(isRef(result.newDocument)).toBeTruthy()
    expect(result.newDocument.value).toBeTypeOf('object')
    expect(result.showEditDocumentModal.value).toBe(false)
    expect(result.remove).toBeTypeOf('function')
  })
})
