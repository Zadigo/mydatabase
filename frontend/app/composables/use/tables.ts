import type { DocumentData } from '~/types'

/**
 * Composables used for working with a table
 * @param table The table
 */
export function useTable(tableName: Ref<string> | string) {
  const dbStore = useDatabasesStore()
  const { currentDatabase } = storeToRefs(dbStore)

  const selectedTable = computed(() => currentDatabase.value?.tables.find(table => table.name === unref(tableName)))

  const tableData = computed(() => selectedTable.value?.documents || [])
  const hasData = computed(() => tableData.value.length > 0)

  return {
    /**
     * The current table
     */
    selectedTable,
    /**
     * The data in the current table
     */
    tableData,
    /**
     * Whether the current table has data
     */
    hasData
  }
}

export type DefaultColumnOption = 'visible' | 'editable' | 'sortable'

export interface ColumnOptions {
  name: string
  visible: boolean
  editable: boolean
  sortable: boolean
}

/**
 * Composables used for working with table columns
 * @param data The table's data
 */
export function useTableColumns(data: DocumentData[] | undefined) {
  const witnessElement = toRef(data?.[0] || {})

  const columnNames = computed(() => Object.keys(witnessElement.value || {}))
  const columnOptions = ref<ColumnOptions[]>(columnNames.value.map(column => ({
    name: column,
    visible: true,
    editable: true,
    sortable: true
  })))

  function toggleOption(column: ColumnOptions, option: DefaultColumnOption) {
    column[option] = !column[option]
  }

  return {
    /**
     * The names of the columns in the table
     */
    columnNames,
    /**
     * The visibility of the columns in the table
     */
    columnOptions,
    /**
     * Toggle the visibility, editability, or sortability of a column
     */
    toggleOption
  }
}
