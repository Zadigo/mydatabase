import { client } from '@/plugins/axios'
import { } from './vue-storages'

function runCallback (func, response) {
  if (typeof func === 'function') {
    func(response.data)
  }
}

export function useSheetsComposable () {
  async function getConnections (callback) {
    // Returns all the sheets that were
    // linked to the app by the user
    try {
      const response = await client.get('sheets')
      runCallback(callback, response)
    } catch (e) {
      console.log(e)
    }
  }

  async function getSheetData (id, callback) {
    // Returns the data for a specific given
    // sheet using the "sheet_id"
    try {
      const response = await client.get(`sheets/${id}`)
      runCallback(callback, response)
    } catch (e) {
      console.log(e)
    }
  }

  async function getBlockData (id) {
    id
  }

  return {
    getBlockData,
    getConnections,
    getSheetData
  }
}


export function useColumnFilters () {
  // A composable for using filters
  
  const defaultOperators = [
    'contains',
    'does not contain...',
    'is',
    'is not',
    'is empty',
    'is not empty',

    'equals',
    'is not equal',
    'greather than',
    'greather than or equal to',
    'less than',
    'less than or equal to'
  ]

  const defaultColumnInputs = [
    'Input',
    'Single select',
    'Multi select',
    'Date'
  ]

  const defaultUnions = [
    'and',
    'or'
  ]

  function createFilter (column, operator, value) {
    if (!defaultOperators.includes(operator)) {
      return {
        column,
        operator: 'contains',
        value
      }
    }
    return {
      column,
      operator,
      value
    }
  }

  return {
    defaultOperators,
    defaultColumnInputs,
    defaultUnions,
    createFilter
  }
}
