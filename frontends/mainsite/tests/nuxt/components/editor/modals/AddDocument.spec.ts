import { mountSuspended } from '@nuxt/test-utils/runtime'
import { createPinia, setActivePinia } from 'pinia'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import AddDocument from '~/components/editor/modals/AddDocument.vue'

vi.mock('~/composables/use/tables/creation', async (original) => {
  // const actual = await vi.importActual<typeof original>('~/composables/use/tables/creation')
  const actual = await original<typeof import('~/composables/use/tables/creation')>()

  return {
    ...actual,
    useCreateDocument: () => ({
      showAddDocumentModal: true
    })
  }
})

describe('Editor > Modals > AddDocument', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('should render modal correctly', async () => {
    const component = await mountSuspended(AddDocument)
    expect(component.html()).toMatchSnapshot()
  })
})
