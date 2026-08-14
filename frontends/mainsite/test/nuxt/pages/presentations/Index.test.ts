import { mountSuspended } from '@nuxt/test-utils/runtime'
import { describe, it, expect } from 'vitest'
import IndexPage from '~/pages/presentations/[id]/index.vue'

describe('Presentations > Presentation > IndexPage', () => {
  it('should render page correctly', () => {
    const component = mountSuspended(IndexPage)
    expect(component).toBeTruthy()
  })
})
