import type { Database, Nullable } from '~/types'

export * from './functions'
export * from './triggers'
export * from './endpoints'
export * from './edition'

export const _useDatabases = createGlobalState(() => {
  const _databases = computedAsync(async () => {
    return await $fetch<Database[]>('/api/databases', {
      method: 'GET'
    })
  })
  const databases = computed(() => _databases.value || [])

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
  const routeId = useRoute().params as { databaseId: string }
  const currentDatabase = useArrayFind<Database>(databases, database => database.id === parseInt(routeId.databaseId))
  
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
    hasTables
  }
})
