import { describe, it, expect } from 'vitest'
import { useEditorPageRefresh } from '../../../app/composables'
import { ref } from 'vue'

describe('useEditorPageRefresh', () => {
  it('should initialize with default params', () => {
    const result = useEditorPageRefresh(ref(null))
    expect(result).toBeDefined()
  })
})
