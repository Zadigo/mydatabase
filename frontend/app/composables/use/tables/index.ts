import type { MaybeTable } from '~/types'

export { useCreateTable } from './creation'
export { useTableWebocketManager } from './ws_manager'

/**
 * Composable that handles how the data is re-integrated
 * in the stores when the page is refreshsed (refreshing the
 * page usually makes the data null)
 * @param currentTable The current table being viewed/edited
 */
export function useEditorPageRefresh(currentTable: MaybeTable) {
  const dbStore = useDatabasesStore()
  const { availableTables } = storeToRefs(dbStore)

  const _currentTable = toRef(currentTable)

  const queryParams = useUrlSearchParams() as { table: string }
  queryParams.table = useToString(isDefined(_currentTable) ? _currentTable.value.id : '').value

  onMounted(() => {
    console.log('params.table', queryParams.table)

    // Load the table to view if specified in the "table" query
    if (queryParams.table) {
      const tableToView = availableTables.value.find(table => table.id === useToNumber(queryParams.table).value)
      console.log('tableToView.value', tableToView)
    }

    // Reload database data on page reload
    const params = useRoute().params as { id: string }
    const id = useToNumber(params.id)

    if (!dbStore.currentDatabase) {
      const databaseToView = dbStore.databases.find(database => database.id === id.value)
      console.log('databaseToView.value', databaseToView)
    }
  })

  if (currentTable) {
    watch(currentTable, (table) => {
      if (table) {
        queryParams.table = useToString(table.id || '').value
      }
    })
  }
}
