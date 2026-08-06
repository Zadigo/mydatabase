import { describe, it, expect } from 'vitest'
import { useDatabaseEndpoints } from '~/composables'

describe('useDatabaseEndpoints', () => {
  it('should initialize with default params', () => {
    const result = useDatabaseEndpoints()
    expect(result).toBeDefined()

    expect(result.create).toBeTypeOf('function')
  })
})
