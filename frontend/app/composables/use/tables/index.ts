import { useAsyncValidator } from '@vueuse/integrations/useAsyncValidator'

import type { Ref } from 'vue'
import type { MaybeTable, SimpleTable } from '~/types'

export {
  useTableWebocketManager
} from './ws_manager'


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

    // Load the table to view if specified in the
    // the "table" query
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
export function useCreateTable(modalState?: Ref<boolean>) {
  const dbStore = useDatabasesStore()

  const [showModal, toggle] = useToggle()

  if (modalState) {
    // If an external state was created for the modal,
    // we can sync it with the local state of showModal
    syncRef(showModal, modalState, { direction: 'both' })
  }

  const newTable = ref<NewTable>({
    name: '',
    database: undefined
  })

  const { errorFields } = useAsyncValidator(newTable, {
    name: {
      type: 'string',
      min: 5,
      max: 20,
      required: true
    }
  })

  const { availableTables } = storeToRefs(useDatabasesStore())

  async function create() {
    newTable.value.database = dbStore.currentDatabase?.id

    const data = await $fetch<SimpleTable>(`/v1/tables/create`, {
      method: 'POST',
      baseURL: useRuntimeConfig().public.prodDomain,
      body: newTable.value
    })

    if (data) {
      availableTables.value.push(data)
      newTable.value.name = ''
      toggle()
    }
  }

  return {
    errorFields,
    showModal,
    newTable,
    toggleCreateDocumentModal: toggle,
    create
  }
}
