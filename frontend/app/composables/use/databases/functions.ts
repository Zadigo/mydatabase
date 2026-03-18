import type { Database } from '~/types/databases'
import type { DatabaseFunction } from '~/types/functions'
import type { Nullable, Undefineable } from '~/types'

/**
 * Function used to manage and create database functions
 */
export const useDatabaseFunctions = createSharedComposable(() => {
  const dbFunctions = ref<DatabaseFunction[]>([])

  function create() {
    dbFunctions.value.push({
      function: {
        name: '',
        table: '',
        columns: [],
        returns: {
          type: 'void',
          value: ''
        },
        chain_to: [],
        signals: {
          failure: {
            do: 'Skip',
            default_value: ''
          }
        }
      }
    })
  }

  /**
   * Search
   */

  const search = ref<string>('')
  const searched = useArrayFilter(dbFunctions, (item) => {
    return item.function.name.toLowerCase().includes(search.value.toLowerCase())
  })

  return {
    dbFunctions,
    search,
    create,
    searched
  }
})

export function useDatabaseFunction(dbFunctions: Ref<DatabaseFunction[]>, databaseFunction: Ref<DatabaseFunction>) {

}

/**
 * Composable used to edit a database function, it manages the state of the edited function and the tables and columns selection
 * @param currentDatabase The current database to which the function belongs to, used to get the tables and columns
 * @param databaseFunction The function to edit, can be a ref or a normal object
 */
export function useEditDatabaseFunction(dbFunctions: Ref<DatabaseFunction[]>, currentDatabase: MaybeRef<Undefineable<Database>>, databaseFunction: MaybeRef<DatabaseFunction>) {
  const editedFunction = ref(databaseFunction)
  const chainTo = ref<boolean>(false)


  const selectedTable = ref<Nullable<number>>(null)

  const tableEditionStore = useTableEditionStore()
  const { selectedTableDocument } = storeToRefs(tableEditionStore)
  const columnNames = computed(() => selectedTableDocument?.value?.column_names || [])

  const otherFunctions = computed(() => {
    const others = useArrayFilter(dbFunctions, (item) => item !== editedFunction.value)
    return others.value.map((func, idx) => `${idx}.${func.function.name}`)
  })

  const shouldReturnDefault = computed(() => editedFunction.value.function.signals.failure.do === 'Default')

  watch(() => editedFunction.value.function.signals.failure.do, (newValue) => {
    if (newValue !== 'Default') {
      editedFunction.value.function.signals.failure.default_value = ""
    }
  })

  return {
    selectedTable,
    editedFunction,
    chainTo,
    columnNames,
    otherFunctions,
    shouldReturnDefault
  }
}
