import type { ColumnOptions, FileCheckoutResponse } from '#shared/types'
import type { NewDocument } from '#shared/types/documents'

const [useDocumentCheckoutProvider, _useDocumentCheckoutStore] = createInjectionState((source: Ref<NewDocument>) => {
  const checkedOut = ref<Record<string, boolean>>({})
  // const fileCheckoutResponse = ref<Record<string, FileCheckoutResponse>>({})

  const fileCheckoutResponse = useSessionStorage<Record<string, FileCheckoutResponse>>('fileCheckoutResponse', {})

  watchDebounced(source, (newValue) => {
    const tableId = useUrlSearchParams('history').table

    if (newValue.documents.length > 0) {
      newValue.documents.forEach((doc, idx) => {
        if (doc.url && !checkedOut.value[doc.url]) {
          const formData = new FormData()
          formData.append('url', doc.url)
  
          checkedOut.value[doc.url] = true
  
          if (doc.file) formData.append('file', doc.file)
  
          $fetch<FileCheckoutResponse>(`/api/tables/${tableId}/checkout`, {
            method: 'POST',
            body: formData
          }).then(response => {
            if (doc.url) {
              fileCheckoutResponse.value[doc.url] = response
              if (source.value.documents[idx]) {
                source.value.documents[idx].column_options = response.columnTypes
              }
            }
          })
        }
      })
    }
  }, {
    deep: true,
    debounce: 3000
  })

  const resetCheckedOut = () => {
    checkedOut.value = {}
  }

  const names = computed(() => Object.keys(checkedOut.value))

  return {
    resetCheckedOut,
    checkedOut,
    fileCheckoutResponse,
    names
  }
})

export { useDocumentCheckoutProvider }

export function useDocumentCheckoutStore() {
  const store = _useDocumentCheckoutStore()
  if (!store) {
    throw new Error('useDocumentCheckoutStore must be used within a provider')
  }
  return store
}
