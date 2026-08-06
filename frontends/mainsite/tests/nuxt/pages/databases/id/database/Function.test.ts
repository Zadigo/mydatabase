import { mountSuspended } from '@nuxt/test-utils/runtime'
import { describe, it, expect } from 'vitest'
import FunctionsPage from '~/pages/databases/[id]/database/functions.vue'

describe('Databases > Database > FunctionsPage', () => {
  it('should render page correctly', async () => {
    const component = await mountSuspended(FunctionsPage)
    expect(component).toBeDefined()
  })
})
