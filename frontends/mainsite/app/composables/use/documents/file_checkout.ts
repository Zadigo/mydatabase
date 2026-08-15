import type { Empty, FileCheckoutResponse, SimpleTable, Undefineable } from '~/types'
import type { DocumentParams, NewDocument } from '.'

const [usePrefetchProvider, _usePrefetchStore] = createInjectionState((selectedTable: WritableComputedRef<Undefineable<SimpleTable>>, newDocument: Ref<NewDocument>) => {
  const fileCheckoutResponse = ref<FileCheckoutResponse | null>(null)
  const columnTypes = computed(() => fileCheckoutResponse.value?.columnTypes || [])

  const prefetch = useDebounceFn(async (documentParams: Empty<DocumentParams>) => {
    console.log('prefetched', documentParams)

    //     const formData = new FormData()

    //     formData.append('name', newDocument.value.name)
    //     formData.append('file', newValue || '')

    //     fileCheckoutResponse.value = await $fetch<FileCheckoutResponse>(`/v1/tables/${selectedTable.value?.id}/checkout`, {
    //       method: 'POST',
    //       baseURL: useRuntimeConfig().public.prodDomain,
    //       body: formData
    //     })
  }, 200)

  return {
    prefetch,
    /**
     * A sample content for what the file contains
     */
    fileCheckoutResponse
  }
})

export { usePrefetchProvider }

export function usePrefetchStore() {
  const store = _usePrefetchStore()

  if (!store) {
    throw new Error('useFileCheckoutStore must be used within a component that calls useFileCheckout')
  }

  return store
}
