import type { Database } from '~/types'

export interface NewDatabase {
  name: string
  description: string
}

/**
 * Composable used to create a new database
 */
export function useDatabaseCreation() {
  const [showModal, toggleCreationModal] = useToggle()

  const newDatabase = ref<NewDatabase>({
    name: '',
    description: ''
  })

  const config = useRuntimeConfig()
  const dbStore = useDatabasesStore()

  function create() {
    const { data } = useFetch<Database>('/v1/databases/create', {
      method: 'POST',
      immediate: true,
      baseURL: config.public.prodDomain,
      body: newDatabase.value
    })

    if (data.value) {
      toggleCreationModal()
      newDatabase.value = { name: '', description: '' }
      dbStore.databases.push(data.value)
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
    toggleCreationModal
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

    if (data.value) {
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
    isUpdating
  }
}
