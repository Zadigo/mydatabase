import type { Database, FileCheckoutResponse, SimpleTable, TableDocument, Undefineable, VueUseWsReturnType } from '~/types'
import type { NewDocument } from '.'
import type { StepperItem } from '@nuxt/ui'

/**
 * Composable used for editing a document
 */
export const useEditDocument = createGlobalState(() => {
  const [showEditDocumentModal, toggleShowEditDocumentModal] = useToggle()

  const tableEditionStore = useTableEditionStore()
  const { tableDocuments } = storeToRefs(tableEditionStore)

  watchDebounced(tableDocuments, async (newValue) => {
    // Update Django with the new column types for each document
    console.log('Updated table documents:', newValue)
  }, { deep: true, debounce: 1000 })

  async function remove(tableDocument: TableDocument) {
    const { status } = await useFetch(`/v1/documents/${tableDocument.document_uuid}`, {
      baseURL: useRuntimeConfig().public.prodDomain,
      method: 'DELETE'
    })

    if (status.value === 'success') {
      tableDocuments.value = tableDocuments.value.filter(doc => doc.id !== tableDocument.id)
    }
  }

  return {
    /**
     * Shows the modal to edit a document
     */
    showEditDocumentModal,
    /**
     * Removes a document from the database
     * @param tableDocument The document to remove
     */
    remove,
    /**
     * Toggles the modal to edit a document
     */
    toggleShowEditDocumentModal
  }
})

/**
 * Composable used for creating a new document
 * @param wsObject The websocket object used to send messages to the server when the document is created. If not provided, the composable will not send any websocket messages. 
 */
export const useCreateDocument = createGlobalState((wsObject?: VueUseWsReturnType) => {
  const [showAddDocumentModal, toggleShowAddDocumentModal] = useToggle()

  const newDocument = ref<NewDocument>({
    name: '',
    url: '',
    google_sheet_id: '',
    file: null,
    entry_key: null,
    using_columns: []
  })

  /**
   * Creates the new document
   */

  const toast = useToast()
  const dbStore = useDatabasesStore()
  const tableEditionStore = useTableEditionStore()
  const { selectedTable } = storeToRefs(tableEditionStore)

  function resetNewDocument() {
    newDocument.value = {
      name: '',
      url: '',
      google_sheet_id: '',
      file: null,
      entry_key: null,
      using_columns: []
    }
  }

  function create() {
    const { data } = useAsyncData('createDocument', async () => {
      const formData = new FormData()

      formData.append('name', newDocument.value.name)
      formData.append('url', newDocument.value.url)
      formData.append('google_sheet_id', newDocument.value.google_sheet_id)
      formData.append('using_columns', JSON.stringify(newDocument.value.using_columns || []))
      formData.append('file', newDocument.value.file || '')

      if (newDocument.value.entry_key) {
        formData.append('entry_key', newDocument.value.entry_key)
      }

      return Promise.all([
        $fetch<{ name: string }>(`/v1/tables/${selectedTable.value?.id}/upload`, {
          method: 'POST',
          baseURL: useRuntimeConfig().public.prodDomain,
          body: formData,
          onResponse({ response }) {
            if (response.status === 200) {
              toggleShowAddDocumentModal()
              resetNewDocument()
            }
          },
          onRequestError(error) {
            toast.add({
              title: 'Failed to add document',
              description: useToString(error).value,
              icon: 'i-lucide-warning-circle'
            })
          }
        }),
        $fetch<Database>(`/v1/databases/${dbStore.currentDatabase?.id}`, {
          method: 'GET',
          baseURL: useRuntimeConfig().public.prodDomain,
          onRequestError(error) {
            toast.add({
              title: 'Failed to retrieve database update',
              description: useToString(error).value,
              icon: 'i-lucide-warning-circle'
            })
          }
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

  const currentStep = ref<StepperItem['title']>('Upload file')

  function updateStep(item: StepperItem) {
    currentStep.value = item.title || ''  
  }

  const canSend = computed(() => isDefined(newDocument.value.file))

  return {
    /**
     * Whether the "Create Document" button can be clicked or not. Only when the user has reached the last step of the stepper, which is "Select columns"
     */
    canSend,
    /**
     * The current step of the stepper when creating a new document
     */
    currentStep,
    /**
     * The new document being created
     */
    newDocument,
    /**
     * Shows the modal to add a new document
     */
    showAddDocumentModal,
    /**
     * Updates the current step of the stepper when creating a new document
     */
    updateStep,
    /**
     * Creates the new document
     */
    create,
    /**
     * Toggles the modal to add a new document
     */
    toggleShowAddDocumentModal
  }
})

const [ useFileCheckout, _useFileCheckoutStore ] = createInjectionState((selectedTable: WritableComputedRef<Undefineable<SimpleTable>>, newDocument: Ref<NewDocument>) => {
  const fileCheckoutResponse = ref<FileCheckoutResponse | null>(null)
  const columnTypes = computed(() => fileCheckoutResponse.value?.columnTypes || [])

  watch(columnTypes, (newValue) => {
    if (newValue) {
      newDocument.value.using_columns = newValue
    }
  })

  watchDebounced(() => newDocument.value.file, async (newValue) => {
    if (isDefined(newValue)) {
      const formData = new FormData()

      formData.append('name', newDocument.value.name)
      formData.append('file', newValue || '')

      fileCheckoutResponse.value = await $fetch<FileCheckoutResponse>(`/v1/tables/${selectedTable.value?.id}/checkout`, {
        method: 'POST',
        baseURL: useRuntimeConfig().public.prodDomain,
        body: formData
      })
    }
  }, { debounce: 2000 })

  return {
    fileCheckoutResponse
  }
})

export { useFileCheckout }

export function useFileCheckoutStore() {
  const store = _useFileCheckoutStore()
  
  if (!store) {
    throw new Error('useFileCheckoutStore must be used within a component that calls useFileCheckout')
  }

  return store
}
