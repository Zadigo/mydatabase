import { describe, it, expect } from 'vitest'
import { useDatabaseCreation } from '../../../app/composables'

describe('useDatabaseCreation', () => {
  it('should initialize with default params', () => {
    const result = useDatabaseCreation()
    expect(result).toBeDefined()
  })
})
