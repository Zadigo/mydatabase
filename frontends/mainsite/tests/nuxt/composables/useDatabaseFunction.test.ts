import { describe, it, expect, beforeEach } from 'vitest'
import { useDatabaseFunction, useDatabaseFunctions } from '../../../app/composables'
import { mountSuspended } from '@nuxt/test-utils/runtime'
import { ref, defineComponent } from 'vue'

describe('useDatabaseFunctions', () => {
  let component: ReturnType<typeof defineComponent> | undefined = undefined
  let result: ReturnType<typeof useDatabaseFunctions> | undefined = undefined

  beforeEach(async () => {
    component = await mountSuspended(defineComponent({
      template: '<div></div>',
      setup() {
        result = useDatabaseFunctions()
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

describe('useDatabaseFunction', () => {
  it('should initialize with default params', () => {
    const result = useDatabaseFunction(ref(null), ref(null))
    expect(result).toBeDefined()
  })
})
