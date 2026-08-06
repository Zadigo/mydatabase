import { mountSuspended } from '@nuxt/test-utils/runtime'
import { describe, it, expect } from 'vitest'
import ConnectionPage from '~/pages/databases/[id]/database/connections.vue'

describe('Databases > Database > ConnectionPage', () => {
  it('should render page correctly', async () => {
    const component = await mountSuspended(ConnectionPage)
    expect(component).toBeDefined()
  })
})
