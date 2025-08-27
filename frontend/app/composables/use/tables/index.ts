import { EditorTablesDataTable } from '#components'
import type { Component } from 'vue'
import type { Database, Table, TableComponent } from '~/types'

export {
  useTableWebocketManager
} from './ws_manager'

/**
 * Composable used to working with a single table
 * @param table The table to manipulate
 */
export function useTable(table: Table | Ref<Table | undefined> | ComputedRef<Table | undefined> | undefined) {
  const componentMapping: Record<TableComponent, Component> = {
    'data-table': EditorTablesDataTable,
    'graph-table': EditorTablesDataTable
  }

  const tableValue = unref(table)
  
  const displayComponent = computed(() => {
    return tableValue ? componentMapping[tableValue.component] : undefined
  })

  const [showEditTableDrawer, toggleEditTableDrawer] = useToggle()
  const editableTableRef = toRef(table) // TODO: Create a unique Ref that is not linked to the original data because when we change the values here it changes the orginal Ref too

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

/**
 * @todo Zod
 */
export interface NewTable {
  name: string
}

/**
 * Composable used to create a new table
 */
export function useCreateTable() {
  const dbStore = useDatabasesStore()

  const showModal = ref<boolean>(false)
  const newTable = ref<NewTable>()

  function create() {
    const { data } = useAsyncData('createDocument', async () => {
      return Promise.all([
        $fetch<{ name: string }>(`/v1/tables/create`, {
          method: 'POST',
          baseURL: useRuntimeConfig().public.prodDomain,
          body: newTable.value
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
    showModal,
    newTable,
    create
  }
}
