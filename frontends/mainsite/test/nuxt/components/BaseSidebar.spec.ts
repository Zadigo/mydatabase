import { describe, it, expect  } from 'vitest'
import { mountSuspended } from '@nuxt/test-utils/runtime'
import BaseSidebar from '~/components/BaseSidebar.vue'
import { definedTestCases } from '~~/test/__mocks__'

describe('BaseSidebar', () => {
  const testCases = definedTestCases((manager) => {
    return manager.parameterize(
      [
        {
          title: 'with no items',
          props: {
            items: undefined
          }
        },
        {
          title: 'with empty array',
          props: {
            items: []
          }
        },
        {
          title: 'with links',
          props: {
            items: [
              {
                name: 'home',
                to: '/',
                icon: 'i-lucide-home',
                separator: false,
                isAlpha: false
              }
            ]
          }
        }
      ]
    )
  })

  testCases.runner.forEach((testCase) => {
    it(`should render correctly ${testCase.title}`, async () => {
      const component = await mountSuspended(BaseSidebar, { props: testCase.props })
      expect(component.html()).toMatchSnapshot()
    })
  })
})
