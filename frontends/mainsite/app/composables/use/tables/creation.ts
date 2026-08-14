import type { SimpleTable } from '~/types'
import type { NewTable } from '~~/shared/types'

/**
 * Composable used to create a new table
 */
export const useCreateTable = createGlobalState(() => {
  const { currentDatabase } = _useDatabases()

  const [showModal, toggleCreateTable] = useToggle()

  const newTable = ref<NewTable>({
    name: '',
    database: undefined
  })


  async function create() {
    const data = await $fetch<SimpleTable>('/api/tables/create', {
      method: 'POST',
      body: {
        ...toValue(newTable),
        database: toValue(currentDatabase)?.id
      }
    })

    if (data) {
      if (isDefined(currentDatabase)) {
        currentDatabase.value.tables.push(data)
      }

      newTable.value.name = ''
      toggleCreateTable()
    }
  }

  return {
    /**
     * Modal state
     */
    showModal,
    /**
     * New table data
     */
    newTable,
    /**
     * Toggle the create table modal
     */
    toggleCreateTable,
    /**
     * Create the new table
     */
    create
  }
})
