import { mountSuspended } from '@nuxt/test-utils/runtime'
import { describe, it, expect } from 'vitest'
import TablesPage from '~/pages/databases/[id]/database/tables.vue'

describe('Databases > Database > TablesPage', () => {
  it('should render page correctly', async () => {
    const component = await mountSuspended(TablesPage)
    expect(component).toBeDefined()
  })
})
