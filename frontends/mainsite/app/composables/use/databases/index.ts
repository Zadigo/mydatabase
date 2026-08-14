import type { Database, Nullable } from '~/types'
import type { DatabaseEndpoint } from '~/types/api/databases/endpoints'

export * from './functions'
export * from './triggers'
export * from './endpoints'

export type NewEndpoint = Pick<DatabaseEndpoint, 'endpoint'>

export interface NewDatabase {
  name: string
  description: string
}

/**
 * Composable used to create a new database
 */
export function useDatabaseCreation() {
  const [showModal, toggle] = useToggle()

  const newDatabase = ref<NewDatabase>({
    name: '',
    description: ''
  })

  const dbStore = useDatabasesStore()

  // TODO: Move to api/server
  async function create() {
    const data = await $fetch<Database>('/v1/databases/create', {
      method: 'POST',
      baseURL: useRuntimeConfig().public.prodDomain,
      body: newDatabase.value
    })

    if (data) {
      dbStore.databases.push(data)
      newDatabase.value = { name: '', description: '' }
      toggle()
    }
  }

  return {
    newDatabase,
    /**
     * Show the database creation modal
     */
    showModal,
    /**
     * Trigger the database creation
     */
    create,
    /**
     * Toggle the database creation modal
     */
    toggleCreationModal: toggle
  }
}

/**
 * Composable used to edit an existing database
 * e.g name, description etc.
 * @param database The database to edit
 */
export function useEditDatabase(database: Ref<Database | undefined>) {
  const config = useRuntimeConfig()

  const newDatabaseName = ref<string>(database.value?.name || '')

  const isUpdating = ref<boolean>(false)
  const toggleIsUpdating = useToggle(isUpdating)
  
  let updated: Database | undefined = undefined

  watchDebounced(newDatabaseName, async () => {
    // await execute()
    toggleIsUpdating(true)

    updated = await $fetch<Database>(`/v1/databases/${database.value?.id}`, {
      baseURL: config.public.prodDomain,
      method: 'POST',
      body: {
        name: newDatabaseName.value
      }
    })

    if (isDefined(updated)) {
      database.value = updated
    }

    toggleIsUpdating(false)
  }, {
    debounce: 1000,
    maxWait: 5000
  })


  return {
    /**
     * The updated database information
     */
    updatedDatabase: updated,
    /**
     * Ref that holds the new database name
     */
    newDatabaseName,
    /**
     * Whether the database is being updated
     */
    isUpdating
  }
}

export const _useDatabases = createGlobalState(() => {
  const _databases = computedAsync(async () => await $fetch<Database[]>('/api/databases', { method: 'GET' }))
  const databases = computed(() => _databases.value || [])

  console.log('databases', databases.value)

  /**
   * Search
   */

  const search = ref<string>('')
  const searched = useArrayFilter<Database>(databases, database => database.name.toLowerCase().includes(search.value.toLowerCase()))

  const params = useUrlSearchParams('history') as { q: string }

  watch(search, (newValue) => {
    if (newValue) {
      params.q = newValue
    } else {
      params.q = ''
    }
  })

  /**
   * Current database
   */

  const routeId = ref<Nullable<number>>(null)
  const currentDatabase = useArrayFind<Database>(databases, database => database.id === routeId.value)

  console.log('currentDatabase', currentDatabase)

  const availableTables = computed(() => isDefined(currentDatabase) ? currentDatabase.value.tables : [])
  const availableTableNames = useArrayMap(isDefined(currentDatabase) ? currentDatabase.value.tables : [], table => table.name)
  const hasTables = computed(() => availableTables.value.length > 0)

  console.log('prodDomain', useRuntimeConfig().public.prodDomain)

  /**
   * Other
   */

  const allTableDocuments = computed(() => {
    if (!isDefined(currentDatabase)) return []
    return currentDatabase.value.tables.flatMap(table => table.documents)
  })

  return {
    /**
     * The documents from all tables in the current database
     * @default []
     */
    allTableDocuments,
    /**
     * List of none-filtered databases
     */
    databases,
    /**
     * The route ID of the currently selected database
     */
    routeId,
    /**
     * The search term used to filter databases
     */
    search,
    /**
     * Filtered list of databases based on the search term
     */
    searched,
    /**
     * The currently selected database
     */
    currentDatabase,
    /**
     * List of available tables in the current database
     * as objects
     */
    availableTables,
    /**
     * The names of the tables in the current database
     */
    availableTableNames,
    /**
     * Whether the database has tables
     * @default false
     */
    hasTables
  }
})
