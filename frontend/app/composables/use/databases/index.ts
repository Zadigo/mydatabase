import type { Database } from '~/types'
import type { DatabaseEndpoint } from '~/types/databases/endpoints'

export * from './functions'

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

  const { data, status, execute } = useFetch<Database>(`/v1/databases/${database.value?.id}`, {
    immediate: false,
    baseURL: config.public.prodDomain,
    body: {
      name: newDatabaseName.value
    }
  })

  watchDebounced(newDatabaseName, async () => {
    await execute()

    if (isDefined(data)) {
      database.value = data.value
    }
  }, {
    debounce: 1000,
    maxWait: 5000
  })

  const isUpdating = computed(() => status.value === 'pending')

  return {
    /**
     * The updated database information
     */
    updatedDatabase: data,
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

export type NewEndpoint = Pick<DatabaseEndpoint, 'endpoint'>

/**
 * Composable used to fetch the endpoints for a database
 * @param database The database to fetch endpoints for
 */
export const useDatabaseEndpoints = createSharedComposable(() => {
  const dbStore = useDatabasesStore()
  const { currentDatabase } = storeToRefs(dbStore)

  const endpoints = ref<DatabaseEndpoint[]>([])

  onMounted(async () => {
    if (isDefined(currentDatabase)) {
      const data = await $fetch<DatabaseEndpoint[]>(`/v1/databases/${currentDatabase.value.id}/endpoints`, {
        baseURL: useRuntimeConfig().public.prodDomain
      })
  
      if (data) {
        endpoints.value = data
      }
    }
  })

  /**
   * New endpoint
   */

  const [showModal, toggleShowModal] = useToggle()
  const newEndpointName = ref<string>('')

  async function create() {
    if (isDefined(currentDatabase)) {
      const data = await $fetch<DatabaseEndpoint[]>(`/v1/endpoints/${currentDatabase.value.id}/create`, {
        method: 'POST',
        baseURL: useRuntimeConfig().public.prodDomain,
        body: { endpoint: newEndpointName.value }
      })

      endpoints.value = data
      toggleShowModal()
    }
  }

  return {
    showModal,
    newEndpointName,
    endpoints,
    toggleShowModal,
    create
  }
})
