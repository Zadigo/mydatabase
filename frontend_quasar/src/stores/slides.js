import { defineStore } from 'pinia'
import _ from 'lodash'

const useSlides = defineStore('store', {
  state: () => ({
    slides: [],
    currentSlide: {}
  }),
  actions: {
    setCurrentSlide (id) {
      this.currentSlide = _.find(this.slides, { slide_id: id }) || {}
    }
  }
})

export {
  useSlides
}
