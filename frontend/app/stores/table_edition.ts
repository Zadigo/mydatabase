import type { DocumentData } from '~/types'

/**
 * Store used to manage the state of table edition
 * accross multiple components aka which table is
 * being edited, what data in the table is being
 * manipulated etc.
 */
export const useTableEditionStore = defineStore('tableEdition', () => {
  const dbStore = useDatabasesStore()
  const { currentDatabase } = storeToRefs(dbStore)

  const selectedTableName = ref<string>()
  const selectedTable = computed(() => currentDatabase.value?.tables.find(table => table.name === selectedTableName.value))

  const tableDocuments = computed(() => selectedTable.value?.documents || [])
  const hasDocuments = computed(() => tableDocuments.value.length > 0)
  
  const selectedTableDocumentName = ref<string>()
  const selectedTableDocument = computed(() => tableDocuments.value.find(doc => doc.name === selectedTableDocumentName.value))
  const selectedTableDocumentNames = computed(() => selectedTable.value?.documents.map(doc => doc.name) || [])

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

export type DefaultColumnOption = 'visible' | 'editable' | 'sortable'

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

  function toggleOption(column: ColumnOptions, option: DefaultColumnOption) {
    column[option] = !column[option]
  }

  const columnTypeOptions = ref<ColumnTypeOptions[]>([])

  function changeTypeOption(column: ColumnTypeOptions, columnType: ColumnType) {
    column.columnType = columnType
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
     */
    toggleOption,
    /**
     * Change the type for the given column
     */
    changeTypeOption
  }
})
