import { describe, it, expect } from 'vitest'
import { useTableWebocketManager } from '../../../app/composables'

describe('useTableWebocketManager', () => {
  it('should initialize with default params', () => {
    const result = useTableWebocketManager()
    expect(result).toBeDefined()
  })
})
