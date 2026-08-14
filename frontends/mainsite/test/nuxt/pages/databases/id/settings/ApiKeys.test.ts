import { mountSuspended } from '@nuxt/test-utils/runtime'
import { describe, it, expect } from 'vitest'
import ApiKeysPage from '~/pages/databases/[id]/settings/api-keys.vue'

describe('Databases > Database > ApiKeysPage', () => {
  it('should render page correctly', async () => {
    const component = await mountSuspended(ApiKeysPage)
    expect(component).toBeDefined()
  })
})
