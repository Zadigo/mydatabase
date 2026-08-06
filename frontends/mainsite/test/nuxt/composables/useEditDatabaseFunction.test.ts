import { describe, it, expect } from 'vitest'
import { useEditDatabaseFunction } from '../../../app/composables'
import { ref } from 'vue'

describe('useEditDatabaseFunction', () => {
  it('should initialize with default params', () => {
    const result = useEditDatabaseFunction(ref(null), ref(null), ref(null))
    expect(result).toBeDefined()
  })
})
