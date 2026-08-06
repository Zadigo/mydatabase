import { describe, it, expect } from 'vitest'
import { useDatabaseTriggers } from '../../../app/composables'

describe('useDatabaseTriggers', () => {
  it('should initialize with default params', () => {
    const result = useDatabaseTriggers()
    expect(result).toBeDefined()
  })
})
