import type { DocumentData, Table, TableComponent } from '~/types'
import { EditorTablesDataTable } from '#components'
import type { Component } from 'vue'

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
 * Composables used for working with table columns
 * @param data The table's data
 */
export function useTableColumns(data: DocumentData[] | undefined) {
  console.log('witnessElement', data)

  const witnessElement = toRef(data?.[0] || {})

  console.log('witnessElement', witnessElement.value)

  const columnNames = computed(() => Object.keys(witnessElement.value || {}))
  const columnOptions = ref<ColumnOptions[]>(columnNames.value.map(column => ({
    name: column,
    visible: true,
    editable: true,
    sortable: true,
    searchable: true
  })))

  function toggleOption(column: ColumnOptions, option: DefaultColumnOption) {
    column[option] = !column[option]
  }

  const columnTypeOptions = ref<ColumnTypeOptions[]>(columnNames.value.map(column => ({
    name: column,
    columnType: 'String',
    unique: false,
    nullable: true
  })))

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
     * The data type of the columns in the table
     */
    columnTypeOptions,
    /**
     * Toggle the visibility, editability, or sortability of a column
     */
    toggleOption
  }
}

/**
 * Composable used to working with a single table
 * @param table The table to manipulate
 */
export function useTable(table: Table | Ref<Table | undefined> | ComputedRef<Table | undefined> | undefined) {
  const componentMapping: Record<TableComponent, Component> = {
    'data-table': EditorTablesDataTable,
    'graph-table': EditorTablesDataTable
  }

  const displayComponent = computed(() => {
    const tableValue = unref(table)
    return tableValue ? componentMapping[tableValue.component] : undefined
  })

  const [showEditTableDrawer, toggleEditTableDrawer] = useToggle()
  const editableTableRef = toRef(table)

  return {
    /**
     * Show drawer for editing the table's data
     */
    showEditTableDrawer,
    /**
     * Reference used to edit table data
     * without modifying the original data
     */
    editableTableRef,
    /**
     * The component used to display the data
     * for the given table
     */
    displayComponent,
    /**
     * Function to toggle the visibility of the edit table drawer
     */
    toggleEditTableDrawer
  }
}
