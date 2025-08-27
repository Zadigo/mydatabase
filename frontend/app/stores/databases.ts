// import { databasesFixture } from '~/data/__fixtures__'
import type { Database } from '~/types'

export const useDatabasesStore = defineStore('databases', () => {
  // const databases = reactive<Database[]>(databasesFixture)
  const databases = ref<Database[]>([])

  console.log('databases', databases.value)

  const search = ref<string>('')
  const searched = computed(() => {
    return databases.value.filter(database => database.name.toLowerCase().includes(search.value.toLowerCase()))
  })

  const routeId = ref<number | null>(null)
  const currentDatabase = computed(() => databases.value.find(database => database.id === routeId.value))
  const availableTables = computed(() => currentDatabase.value?.tables || [])
  const availableTableNames = computed(() => currentDatabase.value?.tables.map(table => table.name) || [])
  const hasTables = computed(() => availableTables.value.length > 0)

  async function fetch() {
    const config = useRuntimeConfig()
    
    const { data, error } = await useFetch<Database[]>('/v1/databases', {
      method: 'GET',
      baseURL: config.public.prodDomain,
      immediate: true
    })

    if (error.value) {
      console.error('Error fetching databases:', error.value)
    }

    if (data.value) {
      databases.value = data.value
    }
  }

  return {
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
