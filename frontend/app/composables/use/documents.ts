import type { ColumnType, Database, SimpleTable, Nullable, PlainOrRef, TableDocument } from '~/types'

export interface NewDocument {
  name: string
  url: string
  google_sheet_id: string
  file: Nullable<Blob>
  entry_key: Nullable<string>
}

/**
 * Get the actual document from a table
 * @param table The table to get the actual document from
 */
export function useTableActualDocument<T extends PlainOrRef<SimpleTable, SimpleTable>>(table: T) {
  const actualTable = ref<T>(table)
  const availableDocuments = computed(() => isDefined(actualTable) ? actualTable.value?.documents : [])
  return useArrayFind<TableDocument>(availableDocuments, (doc) => actualTable.value?.active_document_datasource === doc.document_uuid)
}

export function useColumnTypeOptions() {
  function getTypeIcon(columnType: ColumnType) {
    let icon: string = 'i-lucide-a-large-small'

    switch (columnType) {
      case 'String':
        icon = 'i-lucide-a-large-small'
        break

      case 'Number':
        icon = 'i-lucide-superscript'
        break

      case 'Array':
        icon = 'i-lucide-brackets'
        break

      case 'Boolean':
        icon = 'i-lucide-check'
        break

      case 'Date':
        icon = 'i-lucide-calendar'
        break

      case 'DateTime':
        icon = 'i-lucide-calendar-clock'
        break

      case 'Dict':
        icon = 'i-lucide-braces'
        break

      default:
        break
    }

    return icon
  }

  return {
    getTypeIcon
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
      const formData = new FormData()

      formData.append('name', newDocument.value.name)
      formData.append('url', newDocument.value.url)
      formData.append('google_sheet_id', newDocument.value.google_sheet_id)

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

/**
 * Composable used for editing the state of a document
 * that is not yet saved to the database and is in a temporary state
 */
export function useTempDocument(newDocument: Ref<NewDocument>) {
  const tempColumnsTypes = ref<{ name: string, columnType: ColumnType }[]>([])

  function checkUrl(url: string) {
    // Do something
  }

  watchDebounced(() => newDocument.value.url, (url) => {
    if (url && url.length > 0) {
      checkUrl(url)
    }
  })

  function checkFile() {
    // Do something
  }

  return {
    tempColumnsTypes,
    /**
     * Function that calls the urls and returns the
     * names of the columns in the CSV or JSON NewDocument
     * and their column types
     */
    checkUrl,
    /**
     * Function that reads the file and returns the
     * names of the columns in the CSV or JSON NewDocument
     * and their column types
     */
    checkFile
  }
}

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
 * Composable used for editing the relationships between documents
 */
export function useEditDocumentRelationship() {
  function create() {
    // Do something
  }

  const tableEditionStore = useTableEditionStore()
  const { tableDocuments, selectedTableDocument } = storeToRefs(tableEditionStore)

  // const availableDocuments = computed(() => useArrayFilter(tableDocuments, (doc) => doc.document_uuid !== selectedTableDocument.value?.document_uuid).value)

  /**
   * Columns
   */
 
  const primaryKey = ref<string>()
  const foreignTableId = ref<string>()
  const foreignTableForeignKey = ref<string>()
 
  const primaryKeyColumns = computed(() => isDefined(selectedTableDocument) ? selectedTableDocument.value.column_names : [])
  const foreignTable = useArrayFind(tableDocuments, (doc) => doc.document_uuid === foreignTableId.value)
  const foreignTableColumns = computed(() => isDefined(foreignTable) ? foreignTable.value.column_names : [])

  return {
    primaryKeyColumns,
    foreignTableColumns,
    availableDocuments: tableDocuments,
    /**
     * The primary key of the current document
     */
    primaryKey,
    /**
     * The foreign table id of the related document
     */
    foreignTableId,
    /**
     * The foreign key of the related document
     */
    foreignTableForeignKey,
    /**
     * Creates the relationship between two documents
     */
    create
  }
}
