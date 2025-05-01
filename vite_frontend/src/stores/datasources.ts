import type { AxiosResponse } from 'axios'
import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import { api } from '../plugins'

import type { DataSource, DataSourceDataApiResponse } from '../types'

function runCallback<T extends AxiosResponse<DataSource | DataSource[]>, U extends DataSource | DataSource[]>(response: T, func?: (data: U) => void) {
  if (typeof func === 'function') {
    func(response.data)
  }
}

export const useDatasource = defineStore('datasources', () => {
  /**
   * Contains all the datasources for slides,
   * blocks or other components that use them
   *
   * Connections <-> Slides
   * Connections <-> Blocks
   */
  const connections = ref<DataSource[]>([])

  /**
   * Checks the array has connections
   */
  const hasActiveConnections = computed(() => {
    return connections.value.length > 0
  })

  /**
   * Return all the connection names
   */
  const connectionNames = computed(() => {
    return connections.value.map(connection => connection.name)
  })

  /**
  * Returns all the data sources that were
  * linked to the app by the user. This does not
  * return the underlying data but a description
  * of the data that is linked to a component
  *
  * @param callback
  */
  async function getConnections(callback?: (data: DataSource[]) => void) {
    try {
      const response = await api.get<DataSource[]>('/api/v1/datasources')
      connections.value = response.data
      runCallback(response, callback)
    } catch (e) {
      console.log(e)
    }
  }

  /**
   * Function used to get the datasource for a slide
   * or for a block
   */
  async function requestDatasourceData(dataSource: DataSource, callback?: (data: DataSourceDataApiResponse) => void) {
    try {
      const response = await api.get<DataSourceDataApiResponse>(`/api/v1/datasources/${dataSource.data_source_id}`)

      if (callback) {
        callback(response.data)
      }
    } catch (e) {
      console.log(e)
    }
  }

  return {
    connections,
    connectionNames,
    hasActiveConnections,

    getConnections,
    requestDatasourceData
  }
})
