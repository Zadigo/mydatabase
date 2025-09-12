import type { DatabaseFunction } from '~/types/functions'
import type { SelectItem } from '@nuxt/ui'

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

  return {
    newFunction
  }
}

export function useEditDatabaseFunction(databaseFunction: Ref<DatabaseFunction>) {
  const editedFunction = ref(databaseFunction)

  return {
    editedFunction
  }
}
