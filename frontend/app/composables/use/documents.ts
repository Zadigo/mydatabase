// import { useAsyncValidator } from '@vueuse/integrations/useAsyncValidator'
import type { Database } from '~/types'

export interface NewDocument {
  name: string
  url: string
  google_sheet_id: string
  file: null
  entry_key: null
}

/**
 * Composable used for creating a new document
 */
export function useCreateDocument() {
  const [showAddDocumentModal, toggleShowAddDocumentModal] = useToggle()

  const newDocument = ref<NewDocument>({
    name: '',
    url: '',
    google_sheet_id: '',
    file: null,
    entry_key: null
  })

  const dbStore = useDatabasesStore()
  const tableEditionStore = useTableEditionStore()
  const { selectedTable } = storeToRefs(tableEditionStore)

  // const { data, execute } = useFetch(`/v1/tables/${selectedTable.value?.id}/upload`, {
  //   baseURL: useRuntimeConfig().public.prodDomain,
  //   method: 'POST',
  //   body: newDocument.value,
  //   immediate: false
  // })
  
  function create() {
    const { data } = useAsyncData('createDocument', async () => {
      return Promise.all([
        $fetch<{ name: string }>(`/v1/tables/${selectedTable.value?.id}/upload`, {
          method: 'POST',
          baseURL: useRuntimeConfig().public.prodDomain,
          body: newDocument.value
        }),
        $fetch<Database>(`/v1/databases/${dbStore.currentDatabase?.id}`, {
          method: 'GET',
          baseURL: useRuntimeConfig().public.prodDomain
        })
      ])
    })

    if (data.value) {
      const [createData, databaseUpdateData] = data.value
      console.log(createData)
      console.log(databaseUpdateData)
      // dbStore.databases = databaseUpdateData
    }
  }

  return {
    newDocument,
    showAddDocumentModal,
    create,
    toggleShowAddDocumentModal
  }
}

/**
 * Composable used for editing a document
 */
export function useEditDocument() {
  const [showEditDocumentModal, toggleShowEditDocumentModal] = useToggle()

  return {
    showEditDocumentModal,
    toggleShowEditDocumentModal
  }
}
