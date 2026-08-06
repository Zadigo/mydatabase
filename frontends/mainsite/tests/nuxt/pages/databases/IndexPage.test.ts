import { mockNuxtImport, mountSuspended } from '@nuxt/test-utils/runtime'
import { createPinia, setActivePinia } from 'pinia'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import DatabaseIndexPage from '~/pages/databases/index.vue'
import { NuxtInput } from '#components'

mockNuxtImport('$fetch', () => vi.fn())

describe('IndexPage', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('should render page correctly', async () => {
    const component = await mountSuspended(DatabaseIndexPage)

    const headerEl = component.find('header')
    expect(headerEl).toBeDefined()
    expect(component.find('form')).toBeDefined()
    expect(headerEl.findComponent(NuxtInput)).toBeDefined()
    expect(headerEl.find('button')).toBeDefined()
  })
})
