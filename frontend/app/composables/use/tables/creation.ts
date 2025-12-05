import { useAsyncValidator } from '@vueuse/integrations/useAsyncValidator'
import type { SimpleTable } from '~/types'


/**
 * @todo Zod
 */
export interface NewTable {
  name: string
  database: number | undefined
}

/**
 * Composable used to create a new table
 */
export const useCreateTable = createGlobalState(() => {
  const dbStore = useDatabasesStore()

  const [showModal, toggleCreateTable] = useToggle()

  const newTable = ref<NewTable>({
    name: '',
    database: undefined
  })

  const { errorFields } = useAsyncValidator(newTable, {
    name: {
      type: 'string',
      min: 5,
      max: 20,
      required: true
    }
  })

  const { availableTables } = storeToRefs(useDatabasesStore())

  async function create() {
    newTable.value.database = dbStore.currentDatabase?.id

    const data = await $fetch<SimpleTable>(`/v1/tables/create`, {
      method: 'POST',
      baseURL: useRuntimeConfig().public.prodDomain,
      body: newTable.value
    })

    if (data) {
      availableTables.value.push(data)
      newTable.value.name = ''
      toggleCreateTable()
    }
  }

  return {
    /**
     * Validation errors
     */
    errorFields,
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
