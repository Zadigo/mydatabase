import { mountSuspended } from '@nuxt/test-utils/runtime'
import { createPinia, setActivePinia } from 'pinia'
import { describe, it, expect, beforeEach } from 'vitest'
import BaseNavbar from '~/components/BaseNavbar.vue'

describe('BaseNavbar component', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('should render correctly', async () => {
    const component = await mountSuspended(BaseNavbar)
    // expect(component.html()).toMatchSnapshot()
  })
})
