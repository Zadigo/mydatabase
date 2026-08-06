import { mountSuspended } from '@nuxt/test-utils/runtime'
import { describe, it, expect } from 'vitest'
import IndexPage from '~/pages/index.vue'

describe('IndexPage', { tags: ['nuxt_page'] }, () => {
  it('should render page correctly', async () => {
    const component = await mountSuspended(IndexPage)
    console.log(component.html())
    const linkEl = component.find('a')
    expect(linkEl).toBeDefined()
  })
})
