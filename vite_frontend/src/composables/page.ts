import { api } from "src/boot/axios"
import { defaultColumnInputs, type DefaultOperators, defaultOperators, defaultUnions } from "src/data"

import type { AxiosResponse } from "axios"
import type { DataSource } from "src/types"

function runCallback<T extends AxiosResponse, U extends DataSource | DataSource[]>(func: (data: U) => void, response: T) {
  if (typeof func === 'function') {
    func(response.data)
  }
}

export function useSheetsComposable () {
  /**
   * Returns all the data sources that were
   * linked to the app by the user
   * 
   * @param callback 
   */
  async function getConnections(callback: (data: DataSource[]) => void) { 
    try {
      const response = await api.get<DataSource[]>('/api/v1/datasources')
      runCallback(callback, response)
    } catch (e) {
      console.log(e)
    }
  }

  /**
   * Returns the data for a specific given 
   * sheet using the "sheet_id"
   * 
   * @param id 
   * @param callback 
   */
  async function getSheetData(id: string, callback: (data: DataSource) => void) {
    try {
      const response = await api.get<DataSource>(`/api/V1/datasources/${id}`)
      runCallback(callback, response)
    } catch (e) {
      console.log(e)
    }
  }

  /**
   * @param id 
   */
  async function getBlockData(id: string) {
    // pass
    return id
  }

  return {
    getBlockData,
    getConnections,
    getSheetData
  }
}

/**
 * A composable for using filters 
 */
export function useColumnFilters () {
  /**
   * 
   */
  function createFilter<T extends string | number>(column: string, operator: DefaultOperators, value: T): { column: string, operator: DefaultOperators, value: T } {
    if (!defaultOperators.includes(operator)) {
      return {
        column,
        operator: 'contains',
        value
      }
    } else {
      return {
        column,
        operator,
        value
      }
    }
  }

  return {
    defaultOperators,
    defaultColumnInputs,
    defaultUnions,
    createFilter
  }
}
