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
      newDatabase.value = { name: '', description: '' }
      dbStore.databases.push(data.value)
      toggleCreationModal(true)
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
