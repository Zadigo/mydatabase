import { mountSuspended } from '@nuxt/test-utils/runtime'
import { describe, it, expect } from 'vitest'
import DashboardLayout from '~/layouts/dashboard.vue'
import Navbar from '~/components/BaseNavbar.vue'
import BaseSidebar from '~/components/BaseSidebar.vue'

describe('DashboardLayout', () => {
  it('should render page correctly', async () => {
    const component = await mountSuspended(DashboardLayout)

    expect(component.findComponent(Navbar)).toBeDefined()
    expect(component.findComponent(BaseSidebar)).toBeDefined()
  })
})
