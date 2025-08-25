import { databasesFixture } from '~/data/__fixtures__'
import type { Database } from '~/types'

export const useDatabasesStore = defineStore('databases', () => {
  const databases = reactive(databasesFixture)

  const search = ref<string>('')
  const searched = computed(() => {
    return databases.filter(database => database.name.toLowerCase().includes(search.value.toLowerCase()))
  })

  const routeId = ref<number | null>(null)
  const currentDatabase = computed(() => databases.find(database => database.id === routeId.value))
  const availableTableNames = computed(() => currentDatabase.value?.tables.map(table => table.name) || [])

  async function fetch() {
    const config = useRuntimeConfig()
    
    const { data, error } = await useFetch('/v1/databases', {
      method: 'GET',
      baseURL: config.public.prodDomain,
      immediate: true,
    })

    if (error.value) {
      console.error('Error fetching databases:', error.value)
    }

    return data
  }

  return {
    /**
     * The route ID of the currently selected database
     */
    routeId,
    /**
     * The search term used to filter databases
     */
    search,
    /**
     * The filtered list of databases based on the search term
     */
    searched,
    /**
     * The currently selected database
     */
    currentDatabase,
    /**
     * The names of the tables in the current database
     */
    availableTableNames,
    /**
     * Fetch the list of databases
     */
    fetch
  }
}, {
  persist: {
    pick: ['routeId'],
    storage: sessionStorage
  }
})
