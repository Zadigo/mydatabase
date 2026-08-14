import type { Database } from '~/types'
import type { DatabaseEndpoint } from '~/types/api/databases/endpoints'

export type NewEndpoint = Pick<DatabaseEndpoint, 'endpoint'>

export interface NewDatabase {
  name: string
  description: string
}

/**
 * Composable used to create a new database
 */
export function useDatabaseCreation() {
  const [ showModal, toggle ] = useToggle()

  const newDatabase = ref<NewDatabase>({
    name: '',
    description: ''
  })

  // const dbStore = useDatabasesStore()
  const { push } = _useDatabases() 

  // TODO: Move to api/server
  async function create() {
    // const data = await $fetch<Database>('/v1/databases/create', {
    //   method: 'POST',
    //   baseURL: useRuntimeConfig().public.prodDomain,
    //   body: newDatabase.value
    // })
    
    const data = await $fetch('/api/databases/create', {
      method: 'POST',
      body: newDatabase
    })

    if (data) {
      push(data)
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
