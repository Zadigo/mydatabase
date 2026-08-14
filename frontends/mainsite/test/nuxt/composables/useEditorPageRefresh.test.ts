import { describe, it, expect, beforeEach, vi } from 'vitest'
import { useEditorPageRefresh } from '~/composables/use'
import { createPinia, setActivePinia } from 'pinia'
import { tableFixture } from '../../__fixtures__'

vi.stubGlobal('useRoute', () => ({
  params: {
    id: '1'
  }
}))

describe('useEditorPageRefresh', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('should initialize with default params', () => {
    const result = useEditorPageRefresh(ref(tableFixture))
    expect(result).toBeUndefined()
  })
})
