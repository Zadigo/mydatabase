import { describe, it, expect, beforeEach } from 'vitest'
import { useDatabaseEndpoints } from '../../../app/composables'
import { mountSuspended } from '@nuxt/test-utils/runtime'
import { defineComponent } from 'vue'

describe('useDatabaseEndpoints', () => {
  let component: ReturnType<typeof defineComponent> | undefined = undefined
  let result: ReturnType<typeof useDatabaseEndpoints> | undefined = undefined

  beforeEach(async () => {
    component = await mountSuspended(defineComponent({
      template: '<div></div>',
      setup() {
        result = useDatabaseEndpoints()
        return {
          result
        }
      }
    }))
  })

  it('should initialize with default params', () => {
    expect(component).toBeDefined()
    expect(result).toBeDefined()

    expect(result.create).toBeTypeOf('function')
  })
})
