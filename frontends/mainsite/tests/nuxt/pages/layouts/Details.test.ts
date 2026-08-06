import { mountSuspended } from '@nuxt/test-utils/runtime'
import { describe, it, expect, beforeEach, vi } from 'vitest'
import DetailsLayout from '~/layouts/details.vue'
import Navbar from '~/components/BaseNavbar.vue'
import BaseSidebar from '~/components/BaseSidebar.vue'
import { setActivePinia, createPinia } from 'pinia'

describe('DetailsLayout', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  const asideName: ('editor' | 'database' | 'settings' | 'none')[] = [
    'editor',
    'database',
    'settings',
    'none'
  ]

  asideName.forEach((name) => {
    it(`should render with prop ${name}`, async () => {
      const component = await mountSuspended(DetailsLayout, {
        props: {
          asideName: name
        }
      })
  
      expect(component.findComponent(Navbar)).toBeDefined()
      expect(component.findComponent(BaseSidebar)).toBeDefined()
    })
  })
})
