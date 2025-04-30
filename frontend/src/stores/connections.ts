import _ from 'lodash'
import { defineStore } from 'pinia'


const useConnections = defineStore('connections', {
  state: () => ({
    // Connections <-> Sheets
    connections: [],
    currentConnection: {}
  }),
  getters: {
    hasActiveConnections () {
      // Checks the array has connections
      return this.connections > 0
    },
    connectionNames () {
      // Return all the connection names
      return _.map(this.connections, connection => connection.name)
    }
  },
  actions: {
    async loadFromCache () {
      if (this.connections.length === 0) {
        this.connections = this.$session.retrieve('connections') || []
      }
    },
    setCurrentConnection (sheetId) {
      // Sets the current connection based on the
      // passed sheetId
      this.currentConnection = _.find(this.connections, ['sheet_id', sheetId]) || {}
    }
  }
})

export {
  useConnections
}
