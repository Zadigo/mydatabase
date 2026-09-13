import type { FileCheckoutResponse } from '#shared/types'
import type { NewDocument } from '#shared/types/documents'

export function useDocumentCheckoutCompoable(source: Ref<NewDocument>) {
  const checkedOut = ref<Record<string, boolean>>({})
  const checkedoutResponses = ref<Record<string, FileCheckoutResponse>>({})
  const { table } = useRoute().query as { table: string }

  watchDebounced(source, (newValue) => {
    if (newValue.documents.length > 0) {
      newValue.documents.forEach((doc) => {
        checkedOut.value[ doc.url ] = true

        const formData = new FormData()

        formData.append('url', doc.url)
        if (doc.file) {
          formData.append('file', doc.file)
        }

        $fetch<FileCheckoutResponse>(`/api/tables/${table}/checkout`, {
          method: 'POST',
          body: formData
        }).then(response => {
          if (doc.url) {
            checkedoutResponses.value[ doc.url ] = response
          }
        })

        if (doc.url && !checkedOut.value[ doc.url ]) {
        }
      })
    }
  }, {
    deep: true,
    debounce: 4000
  })

  const resetCheckedOut = () => {
    checkedOut.value = {}
  }

  return {
    resetCheckedOut,
    checkedOut,
    checkedoutResponses
  }
}
