import { mountSuspended } from '@nuxt/test-utils/runtime'
import { describe, it, expect } from 'vitest'
import { usePrefetchProvider, type NewDocument } from '~/composables/use'
import { tableFixture } from '~~/test/__fixtures__'
 
describe('usePrefetchProvider', () => {
  const componentA = defineComponent({
    name: 'ComponentA',
    template: '<div>{{ fileCheckoutResponse }}</div>',
    setup() {
      return usePrefetchStore()
    }
  })

  const componentB = defineComponent({
    name: 'ComponentB',
    components: { componentA },
    template: `
    <div>
      <button id="prefetch-button" @click="prefetch">Prefetch</button>
      <component-a />
    </div>
    `,
    setup() {
      const table = computed({
        get: () => tableFixture,
        set: () => { }
      })

      const newDocument = ref<NewDocument>({
        name: '',
        using_columns: [],
        documents: [],
        merge: false
      })

      return usePrefetchProvider(table, newDocument)
    }
  })

  it('should return default values', async () => {
    const component = await mountSuspended(componentB)
    
    const prefetchButton = component.get('#prefetch-button')

    prefetchButton.trigger('click')
    await component.vm.$nextTick()
  })

  // it('should throw an error if usePrefetchStore is called outside of a component that calls usePrefetchProvider', () => {
  //   expect(() => usePrefetchStore()).toThrow('useFileCheckoutStore must be used within a component that calls useFileCheckout')
  // })
})
