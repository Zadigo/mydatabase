import { describe, it, expect } from 'vitest'
import { useEditDatabase } from '../../../app/composables'
import { ref } from 'vue'

describe('useEditDatabase', () => {
  it('should initialize with default params', () => {
    const result = useEditDatabase(ref(null))
    expect(result).toBeDefined()
  })
})
