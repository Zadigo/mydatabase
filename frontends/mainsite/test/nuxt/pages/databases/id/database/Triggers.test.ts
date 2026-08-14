import { mountSuspended } from '@nuxt/test-utils/runtime'
import { describe, it, expect } from 'vitest'
import TriggersPage from '~/pages/databases/[id]/database/triggers.vue'

describe('Databases > Database > TriggersPage', () => {
  it('should render page correctly', async () => {
    const component = await mountSuspended(TriggersPage)
    expect(component).toBeDefined()
  })
})
