import { mountSuspended } from '@nuxt/test-utils/runtime'
import { describe, it, expect } from 'vitest'
import IndexPage from '~/pages/databases/[id]/settings/index.vue'

describe('Databases > Database > IndexPage', () => {
  it('should render page correctly', async () => {
    const component = await mountSuspended(IndexPage)
    expect(component).toBeDefined()
  })
})
