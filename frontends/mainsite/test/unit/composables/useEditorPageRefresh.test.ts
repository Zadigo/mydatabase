import { describe, it, expect, beforeEach, vi } from 'vitest'
import { useEditorPageRefresh } from '../../../app/composables/use'
import { mountSuspended } from '@nuxt/test-utils/runtime'
import { defineComponent, nextTick } from 'vue'
import { ref } from 'vue'
import { createPinia, setActivePinia } from 'pinia'
import { tableFixture } from '../../__fixtures__/table'

vi.stubGlobal('useRoute', () => ({
  params: {
    id: '1'
  }
}))

describe.todo('useEditorPageRefresh', () => {
  let component: ReturnType<typeof mountSuspended>
  let result: ReturnType<typeof useEditorPageRefresh>

  beforeEach(async () => {
    setActivePinia(createPinia())

    component = await mountSuspended(defineComponent({
      template: `
      <div></div>
      `,
      setup() {
        result = useEditorPageRefresh(ref(tableFixture))
        console.log('result', result)
        return {
          result
        }
      }
    }))

    await nextTick()
  })

  it('should initialize with default params', () => {
    expect(result).toBeDefined()
    expect(component).toBeDefined()

    // Simulate a page refresh by calling the composable again
  })
})
