import { mountSuspended } from '@nuxt/test-utils/runtime'
import { describe, it, expect } from 'vitest'
import EndpointsPage from '~/pages/databases/[id]/settings/endpoints.vue'

describe('Databases > Database > EndpointsPage', () => {
  it('should render page correctly', async () => {
    const component = await mountSuspended(EndpointsPage)
    expect(component).toBeDefined()
  })
})
