import { defineStore } from 'pinia'
import { computed, ref } from 'vue'


export const useConnections = defineStore('connections', () => {
  // Connections <-> Sheets
  const connections = ref([])
  const currentConnection = ref({})

  const hasActiveConnections = computed(() => {
    // Checks the array has connections
    return connections.value.length > 0
  })

  const connectionNames = computed(() => {
    // Return all the connection names
    return connections.value.map(connection => connection.name)
  })

  function loadFromCache() {
    if (connections.value.length === 0) {
      connections.value = $session.retrieve('connections') || []
    }
  }

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
    loadFromCache,
    setCurrentConnection
  }
})
