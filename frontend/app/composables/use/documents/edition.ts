import type { Database, TableDocument } from '~/types'
import type { NewDocument } from '.'

/**
 * Composable used for editing a document
 */
export function useEditDocument() {
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
    entry_key: null,
    using_columns: []
  })

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

      if (newDocument.value.file) {
        formData.append('file', newDocument.value.file)
      }

      if (newDocument.value.entry_key) {
        formData.append('entry_key', newDocument.value.entry_key)
      }

      return Promise.all([
        $fetch<{ name: string }>(`/v1/tables/${selectedTable.value?.id}/upload`, {
          method: 'POST',
          baseURL: useRuntimeConfig().public.prodDomain,
          body: formData
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
