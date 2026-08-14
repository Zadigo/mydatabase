import { describe, it, expect } from 'vitest'
import { useCreateTable } from '~/composables/use/tables'

describe('useCreateTable', () => {
  it('should initialize with default params', () => {
    const result = useCreateTable()
    expect(result).toBeDefined()
  })
})
