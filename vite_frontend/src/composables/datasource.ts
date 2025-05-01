import { api } from '../plugins'

import type { AxiosResponse } from 'axios'
import type { DataSource } from '../types'

function runCallback<T extends AxiosResponse<DataSource | DataSource[]>, U extends DataSource | DataSource[]>(func: (data: U) => void, response: T) {
  if (typeof func === 'function') {
    func(response.data)
  }
}

/**
 * Composable used for retrieving the underlying
 * data from a given souce
 */
export function useDatasourceComposable() {
  /**
   * Returns all the data sources that were
   * linked to the app by the user. This does not
   * return the underlying data but a description
   * of the data that is linked to a component
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
   * sheet using the 'sheet_id'
   * FIXME: Response is rouw data ????
   * @param id The ID of the datasource
   * @param callback Callback function with the actual data
   */
  async function getSheetData(id: string, callback: (data: DataSource) => void) {
    try {
      const response = await api.get<DataSource>(`/api/v1/datasources/${id}`)
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
