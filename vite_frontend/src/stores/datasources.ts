import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

import type { DataSource, Slide } from '../types'

export const useDatasource = defineStore('datasources', () => {
  /**
   * Contains all the datasources for slides,
   * blocks or other components that use them
   *
   * Connections <-> Slides
   * Connections <-> Blocks
   */
  const connections = ref<DataSource[]>([])
  // FIXME: If there are multiple sources then this
  // could be a prolemn
  const currentConnection = ref<DataSource>()

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
   * Sets the current datasource for the
   * current sheet ID
   *
   * @param sheetId
   */
  function setCurrentDatasource(slide: Slide | undefined) {
    if (slide) {
      currentConnection.value = connections.value.find(x => x.data_source_id === slide.slide_data_source.data_source_id)
    }
  }

  return {
    connections,
    currentConnection,
    connectionNames,
    hasActiveConnections,

    setCurrentDatasource
  }
})
