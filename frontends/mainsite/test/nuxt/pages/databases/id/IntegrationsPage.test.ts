import { mountSuspended } from '@nuxt/test-utils/runtime'
import { describe, it, expect } from 'vitest'
import IntegrationsPage from '~/pages/databases/[id]/integrations.vue'

describe('IntegrationsPage', () => {
  it('should render page correctly', async () => {
    const component = await mountSuspended(IntegrationsPage)
    expect(component).toBeDefined()
  })
})
