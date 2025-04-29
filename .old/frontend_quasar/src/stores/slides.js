import { defineStore } from 'pinia'
import _ from 'lodash'

const useSlides = defineStore('store', {
  state: () => ({
    slides: [],
    currentSlide: {},
    currentBlock: {}
  }),
  actions: {
    setCurrentSlide (id) {
      // Sets the currentSlide attribute to the items 
      // of the block that is being currently visited
      this.currentSlide = _.find(this.slides, { slide_id: id }) || {}
    },
    updateBlock (data) {
      // Updates the values of a block in the "blocks"
      // dictionnary key of the current slide
      const block = _.find(this.currentSlide.blocks, { block_id: data.block_id })
      _.forEach(Object.keys(block), (key) => {
        block[key] = data[key]
      })
    }
  }
})

export {
  useSlides
}
