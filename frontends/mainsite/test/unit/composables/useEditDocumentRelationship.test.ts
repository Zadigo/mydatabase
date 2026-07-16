import { describe, it, expect } from 'vitest'
import { useEditDocumentRelationship } from '../../../app/composables'

describe('useEditDocumentRelationship', () => {
  it('should initialize with default params', () => {
    const result = useEditDocumentRelationship()
    expect(result).toBeDefined()
  })
})
