import _ from 'lodash'
import { defineStore } from 'pinia'


// const useSlides = defineStore('slides', {
//   state: () => ({
//     // Connections
//     connections: [],
    
//     // Slide level
//     slides: [],
//     currentSlide: { blocks: [] },
//     currentSlideData: {},

//     // Sheet level
//     currentSheet: null,

//     // Block level
//     currentBlock: {},
//     currentBlockData: {}
//   }),
//   getters: {
//     hasActiveSheet () {
//       // Checks if the slide has an active sheet
//       // or an active connection to a sheet
//       return this.currentSheet !== null
//     },
//     hasLoadedConnections () {
//       // Checks the array has connections
//       return this.connections && this.connections.length > 0
//     },
//     sidebarComponent () {
//       // The sidebar component to use on the slide view
//       const result = this.currentBlock.component && this.currentBlock.component
//       if (result === 'table-block') {
//         return 'table-sidebar'
//       } else if (result === 'chart-block') {
//         return 'chart-sidebar'
//       } else {
//         return 'default-slide-sidebar'
//       }
//     },
//     blockSelected () {
//       // Checks if a block is selected on the slide
//       if (typeof this.currentBlock.component === 'undefined') {
//         return false
//       } else {
//         return true
//       }
//     },
//     blockHasData () {
//       // Checks if the current block actually has data
//       if (typeof this.currentBlockData.id === 'undefined') {
//         return false
//       } else {
//         return true
//       } 
//     },
//     slideHasData () {
//       // Checks if the current slide actually has data
//       if (typeof this.currentSlideData.id === 'undefined') {
//         return false
//       } else {
//         return true
//       } 
//     },
//     availableDataColumns () {
//       // Retuns the columns present in the data
//       return this.availableData.columns || []
//     },
//     availableData () {
//       // Returns the data available to be used
//       // either at the slide level or at the
//       // block level
//       let data = {}
//       if (this.slideHasData) {
//         data = this.currentSlideData
//       } else {
//         data = this.currentBlockData
//       }
//       return data
//     }
//   },
//   actions: {
//     setCurrentSlide (id) {
//       // Sets currentPage to the slide
//       // matching the ID in slides
//       this.loadFromCache()
      
//       if (typeof this.currentSlide.id === 'undefined') {
//         this.currentSlide = _.find(this.slides, ['id', id * 1])
//       }
//     },
//     loadFromCache () {
//       // TODO: When the user lands directly on /slide/2 for example
//       // the session does not have "slides" or "connections" in the 
//       // cache and we need to reload from the backend

//       // Reload some data from the cache: slides, connections
//       if (this.slides.length === 0) {
//         this.slides = this.$session.retrieve('slides') || []
//       }

//       if (this.connections.length === 0) {
//         this.connections = this.$session.retrieve('connections') || []
//       }
//     },
//     getColumnVisibilityCondition (columnName) {
//       // Returns the visibility condition for a specific column
//       return _.find(this.currentBlock.conditions.columns_visibility, ['column', columnName])
//     }
//   }
// })

// export {
//   useSlides
// }

const useSlides = defineStore('slides', {
  state: () => ({
    // Slide level
    slides: [],
    currentSlide: { blocks: [] },
    currentSlideData: {},

    // Sheet level
    currentSheet: null,

    // Block level
    currentBlock: {},
    currentBlockData: {},

    // Container that stores changes 
    // upon a given block and shares
    // the changes between components
    blockRequestData: {
      name: null,
      record_creation_columns: [],
      record_update_columns: [],
      allow_record_creation: true,
      allow_record_search: true,
      allow_record_update: true,
      block_data_source: null,
      search_columns: [],
      user_filters: [],
      visible_columns: [],
      conditions: {
        filters: [],
        groups: []
      },
      active: true,
    }
  }),
  getters: {
    requiresSave () {
      // Checks if user needs to click save either at the slide
      // level or at the block level
      return _.some([this.slideRequiresSave, this.blockRequiresSave], x => x === true)
    },
    blockSelected () {
      // Checks if a block was selected in a slide
      if (typeof this.currentBlock.block_id === 'undefined') {
        return false
      } else {
        return true
      }
    },
    hasActiveBlocks () {
      // Checks if the current slide has blocks
      return this.currentSlide.blocks.length > 0
    },
    slideHasData () {
      // Checks if data is currently loaded
      // on the slide level
      return Object.keys(this.currentSlideData).length > 0
    },
    blockHasData () {
      // Checks if data is currently loaded
      // on the block level 
      return Object.keys(this.currentBlockData).length > 0
    },
    dataToUse () {
      // Returns either the slide level data
      // or the block level data
      if (this.blockHasData) {
        return this.blockHasData
      }

      if (this.slideHasData) {
        return this.currentSlideData
      }

      return {}
    },
    activeSidebarComponent () {
      // The active sidebar component to use 
      // when navigating the SlideView
      let component = 'default-slide-sidebar'

      switch (this.currentBlock.component) {
        case 'table-block':
          component = 'table-sidebar'
          break

        case 'chart-block':
          component = 'chart-sidebar'
          break
      
        default:
          break
      }
      return component
    }
  },
  actions: {
    loadFromCache () {
      // TODO: When the user lands directly on /slide/2 for example
      // the session does not have "slides" or "connections" in the
      // cache and we need to reload from the backend

      // Reload some data from the cache
      if (this.slides.length === 0) {
        this.slides = this.$session.retrieve('slides') || []
      }
    },
    setCurrentBlockRequestData () {
      // Set the current values for the
      // in the requestData for the current
      // selected block
      if (this.blockSelected) {
        Object.keys(this.blockRequestData).forEach((key) => {
          this.blockRequestData[key] = this.currentBlock[key]
        })
      }
    },
    setCurrentSlide (id) {
      // Sets currentSlide to the slide
      // matching the ID in slides
      this.loadFromCache()
      
      if (typeof this.currentSlide.id === 'undefined') {
        this.currentSlide = _.find(this.slides, ['id', id * 1])
      }
    },
    setCurrentSlideData (slideId, data) {
      this.currentSlideData = data.results
      this.$session.create(slideId, data.results)
    },
    resetBlockRequestData () {
      // Reset the modifications made
      // to the blockRequestData
      this.slideRequiresSave = false
      this.blockRequiresSave = false
      this.blockRequestData = {
        name: null,
        allow_record_creation: true,
        allow_record_updates: true,
        block_data_source: null,
        search_columns: [],
        user_filters: [],
        active: true,
        conditions: {
          filters: [],
          columns_visibility: []
        }
      }
    }
  }
})

export {
  useSlides
}
