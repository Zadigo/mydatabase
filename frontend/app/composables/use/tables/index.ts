import { EditorTablesDataTable } from '#components'
import type { Component, MaybeRef } from 'vue'
import type { Database, SimpleTable, TableComponent } from '~/types'

export {
  useTableWebocketManager
} from './ws_manager'


type MaybeTable = MaybeRef<SimpleTable | undefined> | ComputedRef<SimpleTable | undefined> | undefined

/**
 * Composable used to working with a single table such as
 * table edition the display component to show etc.
 * @param table The table to manipulate
 */
export function useTable(table: MaybeTable) {
  const componentMapping: Record<TableComponent, Component> = {
    'data-table': EditorTablesDataTable,
    'graph-table': EditorTablesDataTable
  }

  const tableValue = unref(table)
  
  const displayComponent = computed(() => {
    return tableValue ? componentMapping[tableValue.component] : undefined
  })

  const [ showEditTableDrawer, toggleEditTableDrawer ] = useToggle()
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
 * Composable that handles how the data is re-integrated
 * in the stores when the page is refreshsed (refreshing the
 * page usually makes the data null)
 * @param currentTable The current table being viewed/edited
 */
export function useEditorPageRefresh(currentTable: MaybeTable) {
  const dbStore = useDatabasesStore()
  const { availableTables } = storeToRefs(dbStore)

  const queryParams = useUrlSearchParams() as { table: string }
  queryParams.table = useToString(currentTable.value?.id || '').value

  onMounted(() => {
    console.log('params.table', queryParams.table)

    // Load the table to view if specified in the
    // the "table" query
    if (queryParams.table) {
      const tableToView = availableTables.value.find(table => table.id === useToNumber(queryParams.table).value)
      console.log('tableToView.value', tableToView.value)
    }

    // Reload database data on page reload
    const params = useRoute().params as { id: string }
    const id = useToNumber(params.id)

    if (!dbStore.currentDatabase) {
      const databaseToView = dbStore.databases.find(database => database.id === id.value)
      console.log('databaseToView.value', databaseToView.value)
    }
  })

  if (currentTable) {
    watch(currentTable, (value) => {
      if (value) {
        queryParams.table = useToString(value.id || '').value
      }
    })
  }
}

/**
 * @todo Zod
 */
export interface NewTable {
  name: string
  database: number | undefined
}

/**
 * Composable used to create a new table
 */
export function useCreateTable() {
  const dbStore = useDatabasesStore()

  const [showModal, toggleCreateDocumentModal] = useToggle()
  const newTable = ref<NewTable>({
    name: '',
    database: undefined
  })

  async function create() {
    newTable.value.database = dbStore.currentDatabase?.id

    const { data } = await useAsyncData('createTable', async () => {
      return Promise.all([
        $fetch<SimpleTable>(`/v1/tables/create`, {
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
      const [newTableData, updatedDatabase] = data.value
      showModal.value = false
      newTable.value = { name: '', database: undefined }
      // toggleCreateDocumentModal()
      // dbStore.databases = updatedDatabase
      console.log(updatedDatabase)
    }
  }

  return {
    showModal,
    newTable,
    toggleCreateDocumentModal,
    create
  }
}
