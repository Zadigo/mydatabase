import { api } from '../plugins'

import type { AxiosResponse } from 'axios'
import type { DataSource, DataSourceDataApiResponse } from '../types'

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
   * Returns the underlying data for a specific given
   * datasource ID
   *
   * @param id The ID of the datasource
   * @param callback Callback function with the actual data
   */
  async function getDatasourceData(datasourceId: string, callback: (data: DataSourceDataApiResponse) => void) {
    try {
      if (datasourceId) {
        const response = await api.get<DataSourceDataApiResponse>(`/api/v1/datasources/${datasourceId}`)
        callback(response.data)
      }
    } catch (e) {
      console.log(e)
    }
  }

  return {
    getConnections,
    getDatasourceData
  }
}
