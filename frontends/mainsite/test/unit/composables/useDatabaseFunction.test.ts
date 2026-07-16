import { describe, it, expect } from 'vitest'
import { useDatabaseFunction, useDatabaseFunctions } from '../../../app/composables'
import { ref } from 'vue'

describe('useDatabaseFunctions', () => {
  it('should initialize with default params', () => {
    const result = useDatabaseFunctions()
    expect(result).toBeDefined()
  })
})

describe('useDatabaseFunction', () => {
  it('should initialize with default params', () => {
    const result = useDatabaseFunction(ref(null), ref(null))
    expect(result).toBeDefined()
  })
})
