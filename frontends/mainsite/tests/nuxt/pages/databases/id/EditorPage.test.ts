import { mockNuxtImport, mountSuspended } from '@nuxt/test-utils/runtime'
import type { UseWebSocketOptions } from '@vueuse/core'
import { describe, it, expect, vi } from 'vitest'
import EditorPage from '~/pages/databases/[id]/editor.vue'

mockNuxtImport('useRoute', original => vi.fn(original))

vi.mock('@vueuse/core', async () => {
  const actual = await vi.importActual<typeof import('@vueuse/core')>('@vueuse/core')
  return {
    ...actual,
    useWebSocket: vi.fn<typeof import('@vueuse/core')['useWebSocket']>((url: MaybeRefOrGetter<string | URL | undefined>, options?: UseWebSocketOptions) => ({
      open: vi.fn(),
      close: vi.fn(),
      status: { value: 'OPEN' },
      send: vi.fn(),
      data: ref({ value: '' }),
      ws: { value: undefined }
    }))
  }
})

describe('EditorPage', () => {
  it('should render page correctly', async () => {
    const component = await mountSuspended(EditorPage)
    expect(component).toBeDefined()
  })
})
