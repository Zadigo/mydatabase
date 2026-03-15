import type { Database, TableDocument, VueUseWsReturnType } from '~/types'
import type { NewDocument } from '.'

/**
 * Composable used for editing a document
 */
export const useEditDocument = createGlobalState(() => {
  const [showEditDocumentModal, toggleShowEditDocumentModal] = useToggle()

  const tableEditionStore = useTableEditionStore()
  const { tableDocuments } = storeToRefs(tableEditionStore)

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

  return {
    /**
     * The new document being created
     */
    newDocument,
    /**
     * Shows the modal to add a new document
     */
    showAddDocumentModal,
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
