import { defineStore } from 'pinia'
import { type Connection } from 'src/types/connections'
import { computed, ref } from 'vue'


export const useConnections = defineStore('connections', () => {
  // Connections <-> Sheets
  const connections = ref<Connection[]>([])
  const currentConnection = ref<Connection>()

  const hasActiveConnections = computed(() => {
    // Checks the array has connections
    return connections.value.length > 0
  })

  const connectionNames = computed(() => {
    // Return all the connection names
    return connections.value.map(connection => connection.name)
  })

  /**
   * Sets the current connection based on the
   * passed sheetId
   * 
   * @param sheetId 
   */
  function setCurrentConnection (sheetId: string) {
    currentConnection.value = connections.value.find(['sheet_id', sheetId]) || {}
  }

  return {
    connections,
    currentConnection,
    connectionNames,
    hasActiveConnections,
    setCurrentConnection
  }
})
