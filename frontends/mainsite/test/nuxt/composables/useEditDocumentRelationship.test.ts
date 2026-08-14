import { describe, it, expect } from 'vitest'
import { useEditDocumentRelationship } from '~/composables'

describe('useEditDocumentRelationship', () => {
  it('should initialize with default params', () => {
    const result = useEditDocumentRelationship()
    expect(result).toBeDefined()
  })
})
