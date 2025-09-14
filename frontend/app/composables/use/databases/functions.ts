import type { Database } from '~/types/databases'
import type { DatabaseFunction } from '~/types/functions'
import type { SelectItem } from '@nuxt/ui'
import type { RefOrUndefined } from '~/types'

export const selectFunctionMenuItems = ref<SelectItem[]>([
  {
    type: 'label',
    label: 'Aggegrate'
  },
  'Count',
  'Sum',
  'Avg',
  'Min',
  'Max',
  {
    type: 'separator'
  },
  {
    type: 'label',
    label: 'String'
  },
  'Upper',
  'Lower',
  'Length',
  'Trim',
  'Group concat',
  'Coalesce',
  'Extract',
  {
    type: 'separator'
  },
  {
    type: 'label',
    label: 'Date'
  },
  'Now',
  'Date',
  'Time',
  'Datetime',
  'Strftime',
  'Current timestamp',
  'Current date',
  'Current time',
  {
    type: 'separator'
  },
  {
    type: 'label',
    label: 'Miscellanous'
  },
  'Random',
  'MD5',
  'SHA256',
  'SHA512'
])

export const useDatabaseFunctions = createSharedComposable(() => {
  const dbFunctions = ref<DatabaseFunction[]>([])

  function create() {
    dbFunctions.value.push({
      function: {
        name: 'Lower',
        table: '',
        columns: [],
        returns: {
          type: 'void',
          value: null
        },
        chain_to: [],
        failure: {
          on: 'Skip',
          default_value: null
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

export function useCreateDatabaseFunction() {
  const newFunction = ref<DatabaseFunction>({
    name: 'Lower',
    table: null,
    columns: [],
    returns: {
      value: null,
      type: 'void'
    },
    chain_to: [],
    on_fail: {
      do: 'Skip',
      default_value: null
    }
  })

  return {
    newFunction
  }
}

export function useEditDatabaseFunction(currentDatabase: RefOrUndefined<Database>, databaseFunction: DatabaseFunction | Ref<DatabaseFunction>) {
  const editedFunction = ref(databaseFunction)
  const chainTo = ref<boolean>(false)

  const selectedTable = useArrayFind(currentDatabase.value?.tables || [], (table) => table.id === editedFunction.value.table)

  return {
    selectedTable,
    chainTo,
    editedFunction
  }
}
