import type { DocumentData, SimpleTable } from '~/types'

/**
 * Store used to manage the state of table edition
 * across multiple components aka which table is
 * being edited, what data in the table is being
 * manipulated etc.
 */
export const useTableEditionStore = defineStore('tableEdition', () => {
  const dbStore = useDatabasesStore()
  const { currentDatabase } = storeToRefs(dbStore)

  /**
   * Table selection
   */

  const selectedTableName = ref<string>()
  const selectedTable = computed({ get: () => currentDatabase.value?.tables.find(table => table.name === selectedTableName.value), set: (value) => value })

  // When the TableDocument already has a datasource
  // we need to automatically set the value on the
  // select input when the user selects that table
  watch(selectedTable, (value) => {
    if (value) {
      if (value.active_document_datasource) {
        const tableDocument = tableDocuments.value.find(doc => doc.document_uuid === value.active_document_datasource)
        if (tableDocument) {
          selectedTableDocumentName.value = tableDocument.name
        }
      }
    }
  })

  /**
   * Documents
   */

  const tableDocuments = computed({ get: () => isDefined(selectedTable) ? selectedTable.value.documents : [], set: (value) => value })
  const hasDocuments = computed(() => tableDocuments.value.length > 0)
  
  const selectedTableDocumentName = ref<string>()
  const selectedTableDocument = useArrayFind(tableDocuments, (doc) => doc.name === selectedTableDocumentName.value)
  const selectedTableDocumentNames = computed(() => useArrayMap(isDefined(selectedTable) ? selectedTable.value.documents : [], doc => doc.name).value)

  // When the user changes the selection of the datasoure,
  // automatically update the selection on Django
  watchDebounced(selectedTableDocumentName, async (newSelectedName) => {
    if (isDefined(selectedTable) && isDefined(selectedTableDocument)) {
      if (selectedTableDocument.value.name === newSelectedName) {
        return
      }

      const data = await $fetch<SimpleTable>(`/v1/tables/${selectedTable.value.id}`, {
        method: 'PATCH',
        baseURL: useRuntimeConfig().public.prodDomain,
        body: {
          active_document_datasource: selectedTableDocument.value.document_uuid
        }
      })
  
      if (data) {
        selectedTable.value = data
      }
    }
  }, {
    immediate: false,
    debounce: 4000
  })

  /**
   * Data
   */

  const tableData = ref<DocumentData[]>([])
  const hasData = computed(() => tableData.value.length > 0)
  
  return {
    /**
     * The current table
     */
    selectedTable,
    /**
     * The name of the selected table
     */
    selectedTableName,
    /**
     * The name of the selected document
     * for the current table
     */
    selectedTableDocumentName,
    /**
     * List of available documents by name
     * @description This is useful essentially for autocompletion
     */
    selectedTableDocumentNames,
    /**
     * The currently selected document as an object
     */
    selectedTableDocument,
    /**
     * The documents contained within the selected table
     */
    tableDocuments,
    /**
     * The actual data to use for the current table
     */
    tableData,
    /**
     * Whether the current table has any data
     */
    hasData,
    /**
     * Whether the current table has at least
     * one document linked to it
     */
    hasDocuments
  }
}, {
  persist: {
    pick: ['selectedTableName', 'selectedTableDocumentName'],
    storage: sessionStorage
  }
})

export type DefaultColumnOption = 'visible' | 'editable' | 'sortable' | 'searchable'

export interface ColumnOptions {
  name: string
  visible: boolean
  editable: boolean
  sortable: boolean
  searchable: boolean
}

export const columnTypes = [
  'String',
  'Number',
  'Boolean',
  'Date',
  'DateTime',
  'Array',
  'Dict'
] as const

export type ColumnType = typeof columnTypes[number]

export const columnTypesMenuItem: { label: ColumnType; icon: string }[] = [
  {
    label: 'String',
    icon: 'i-lucide-text'
  },
  {
    label: 'Number',
    icon: 'i-lucide-superscript'
  },
  {
    label: 'Boolean',
    icon: 'i-lucide-check-square'
  },
  {
    label: 'Date',
    icon: 'i-lucide-calendar'
  },
  {
    label: 'DateTime',
    icon: 'i-lucide-clock'
  },
  {
    label: 'Array',
    icon: 'i-lucide-list'
  },
  {
    label: 'Dict',
    icon: 'i-lucide-folder'
  }
]

export interface ColumnTypeOptions {
  /**
   * The column's name
   */
  name: string
  /**
   * The data type for this column
   * @default "String"
   */
  columnType: ColumnType,
  /**
   * Column values should be unique
   * @default false
   */
  unique: boolean
  /**
   * Column an be null
   * @default true
   */
  nullable: boolean
}

/**
 * Store used for working with table columns
 * e.g. search, modifying column types etc.
 */
export const useTableColumnsStore = defineStore('tableColumns', () => {
  const columnNames = ref<string[]>([])
  const columnOptions = ref<ColumnOptions[]>([])

  const tableStore = useTableEditionStore()
  const { selectedTableDocument } = storeToRefs(tableStore)


  /**
   * Column options
   */

  function toggleOption(column: ColumnOptions, option: DefaultColumnOption) {
    column[option] = !column[option]

    if (isDefined(selectedTableDocument)) {
      $fetch(`/v1/documents/${selectedTableDocument.value.id}/column-types`, {
        method: 'patch',
        baseURL: useRuntimeConfig().public.prodDomain,
        body: {
          column_options: columnOptions.value
        }
      })
    }
  }

  const columnTypeOptions = ref<ColumnTypeOptions[]>([])

  function changeTypeOption(column: ColumnTypeOptions, columnType: ColumnType) {
    column.columnType = columnType
  }

  function toggleConstraint(column: ColumnTypeOptions, constraint: 'unique' | 'nullable') {
    column[constraint] = !column[constraint]
  }

  /**
   * Column types
   */

  function save() {
    if (isDefined(selectedTableDocument)) {
      $fetch(`/v1/documents/${selectedTableDocument.value.id}/column-types`, {
        method: 'patch',
        baseURL: useRuntimeConfig().public.prodDomain,
        body: {
          column_types: columnTypeOptions.value
        }
      })
    }
  }

  return {
    /**
     * The names of the columns in the table
     */
    columnNames,
    /**
     * Options for modifying how the end user interacts
     * with the columns e.g visibility, editability, sortability
     */
    columnOptions,
    /**
     * Options for modifiying the data types of each column
     */
    columnTypeOptions,
    /**
     * Toggle the visibility, editability, or sortability of a column
     * @param column The column to modify
     * @param option The option to toggle
     */
    toggleOption,
    /**
     * Change the type for the given column
     */
    changeTypeOption,
    /**
     * Change the constraint type of the column
     */
    toggleConstraint,
    /**
     * Persist the column settings to the backend
     */
    save
  }
}, {
  persist: {
    pick: ['columnNames', 'columnOptions', 'columnTypeOptions'],
    storage: sessionStorage
  }
})
