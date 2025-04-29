import { defineStore } from "pinia";

const usePublishedSlides = defineStore('published_slides', {
  state: () => ({
    slides: [],
    isPreview: false,

    currentSlide: {},
    currentSlideData: {}
  })
})

export {
  usePublishedSlides
}
