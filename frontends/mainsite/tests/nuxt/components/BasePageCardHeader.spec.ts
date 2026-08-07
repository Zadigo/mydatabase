import { mountSuspended } from '@nuxt/test-utils/runtime'
import { describe, it, expect } from 'vitest'
import BasePageCardHeader from '~/components/BasePageCardHeader.vue'
import type { TestCase } from '../../setup'

describe('BasePageCardHeader component', () => {
  const cases: TestCase<{
    title: string
    placeholder: string
    actionName: string
  }>[] = [
    {
      title: 'should render correctly with default props',
      props: {
        title: 'Test Title',
        placeholder: 'Test Placeholder',
        actionName: 'Test Action'
      }
    }
  ]

  cases.forEach(({ title, props }) => {
    it(title, async () => {
      const component = await mountSuspended(BasePageCardHeader, { props })

      expect(component.find('h3')).toBeDefined()
      expect(component.find('h3').text()).toEqual(props.title)

      expect(component.find('input[type="search"]')).toBeDefined()
      expect(component.find('input[type="search"]').attributes('placeholder')).toEqual(props.placeholder)
    })
  })
})
