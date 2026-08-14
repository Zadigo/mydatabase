import { mountSuspended } from '@nuxt/test-utils/runtime'
import { describe, it, expect } from 'vitest'
import BaseColumnTypeOption from '~/components/BaseColumnTypeOption.vue'
import { columnTypeOptionsFixture } from '~~/test/__fixtures__'
import type { ColumnTypeOptions } from '~/types'

describe.todo('BaseColumnTypeOption component', () => {
  const testCases: { title: string, props: { columnType: ColumnTypeOptions | undefined } }[] = [
    {
      title: 'default props',
      props: {
        columnType: columnTypeOptionsFixture
      }
    },
    {
      title: 'undefined columnType',
      props: {
        columnType: undefined
      }
    }
  ]

  testCases.forEach((testCase) => {
    it(`should render correctly with ${ testCase.title }`, async () => {
      const component = await mountSuspended(BaseColumnTypeOption, { props: testCase.props })
      // expect(component.html()).toMatchSnapshot()
    })
  })
})
