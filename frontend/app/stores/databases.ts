import type { Database, Nullable, TableDocument } from '~/types'

/**
 * Store for managing databases and their tables.
 * Provides functionality to fetch databases, filter them by search term,
 * and access details of the currently selected database.
 */
export const useDatabasesStore = defineStore('databases', () => {
  const databases = ref<Database[]>([])

  console.log('databases', databases.value)

  /**
   * Search
   */

  const search = ref<string>('')
  const searched = useArrayFilter<Database>(databases, (database) => database.name.toLowerCase().includes(search.value.toLowerCase()))

  /**
   * Current database
   */

  const routeId = ref<Nullable<number>>(null)
  const currentDatabase = useArrayFind<Database>(databases, (database) => database.id === routeId.value)
  
  console.log('currentDatabase', currentDatabase)
  
  const availableTables = computed(() => isDefined(currentDatabase) ? currentDatabase.value.tables : [])
  const availableTableNames = useArrayMap(isDefined(currentDatabase) ? currentDatabase.value.tables : [], table => table.name)
  const hasTables = computed(() => availableTables.value.length > 0)

  async function fetch() {
    const data = await $fetch<Database[]>('/v1/databases', {
      method: 'GET',
      baseURL: useRuntimeConfig().public.prodDomain
    })

    if (data) {
      databases.value = data
    }
  }

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
     * Fetch the list of databases
     */
    fetch
  }
}, {
  persist: {
    pick: ['routeId', 'databases'],
    storage: sessionStorage
  }
})
