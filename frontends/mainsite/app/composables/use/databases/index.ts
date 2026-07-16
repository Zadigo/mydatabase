import type { Database } from '~/types'
import type { DatabaseEndpoint } from '~/types/api/databases/endpoints'

export * from './functions'
export * from './triggers'

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
      endpoints.value = await $fetch<DatabaseEndpoint[]>(`/v1/databases/${currentDatabase.value.id}/endpoints`, {
        baseURL: useRuntimeConfig().public.prodDomain
      })
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
