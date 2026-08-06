import { mountSuspended } from '@nuxt/test-utils/runtime'
import { describe, it, expect } from 'vitest'
import SettingsPage from '~/pages/settings/index.vue'

describe('Settings > IndexPage', () => {
  it('should render page correctly', async () => {
    const component = await mountSuspended(SettingsPage)
    expect(component).toBeDefined()
  })
})
