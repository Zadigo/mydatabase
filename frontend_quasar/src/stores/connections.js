import _ from 'lodash'
import { defineStore } from "pinia"

const useDataSources = defineStore('datasources', {
  state: () => ({
    dataSources: [],
    currentSlideDataSource: {}
  }),
  getters: {
    sourcesIds () {
      return _.map(this.dataSources, (item) => {
        return {
          name: item.name,
          source_id: item.sheet_id
        }
      })
    }
  },
  actions: {
    setCurrentDataSource (id) {
      console.log(id)
      this.currentSlideDataSource = _.find(this.dataSources, { sheet_id: id }) || {}
    }
  }
})

export {
  useDataSources
}
