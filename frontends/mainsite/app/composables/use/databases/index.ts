import type { Database } from '~/types'

export * from './functions'
export * from './triggers'
export * from './endpoints'
export * from './edition'

export const _useDatabases = createGlobalState(() => {
  // const _databases = computedAsync(async () => {
  //   return await $fetch<Database[]>('/api/databases', {
  //     method: 'GET'
  //   })
  // })

  // // const databases = computed(() => _databases.value || [])
  // const databases = computed({
  //   get: () => _databases.value || [],
  //   set: (value) => {
  //     value.push()
  //   }
  // })

  const { state, execute } = useAsyncState(
    () => $fetch<Database[]>('/api/databases', { method: 'GET' }),
    [],
    {
      immediate: true,
      resetOnExecute: false
    }
  )

  // Local mutable source of truth
  const localMutableDatabases = ref<Database[]>([])

  // Sync fetched data into local state whenever a fetch resolves
  watch(state, (value) => {
    localMutableDatabases.value = value ?? []
  })

  const databases = computed<Database[]>({
    get: () => localMutableDatabases.value,
    set: (value) => {
      localMutableDatabases.value = value
    }
  })

  async function refresh() {
    await execute()
  }

  function push(database: Database) {
    localMutableDatabases.value = [ ...localMutableDatabases.value, database ]
  }

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

  // const routeId = ref<Nullable<number>>(null)
  // const routeId = useRoute().params as { id: string }
  const routeId = computed(() => useRoute().params as { id: string })
  console.log('routeId', useRoute, routeId.value)
  const currentDatabase = useArrayFind<Database>(databases, database => database.id === parseInt(routeId.value.id))
  
  const availableTables = computed(() => isDefined(currentDatabase) ? currentDatabase.value.tables : [])
  const availableTableNames = useArrayMap(isDefined(currentDatabase) ? currentDatabase.value.tables : [], table => table.name)
  const hasTables = computed(() => availableTables.value.length > 0)

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
    hasTables,
    /**
     * Refresh the database data
     */
    refresh,
    /**
     * Push a newly created database in the existing ones
     */
    push
  }
})
