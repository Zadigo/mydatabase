import { defineStore } from "pinia"
import { ref } from "vue"

import type { RowData, Slide } from "src/types"

export const usePublishedSlides = defineStore('published_slides', () => {
  const slides = ref<Slide[]>([])
  const isPreview = ref<boolean>(false)

  const currentSlide = ref<Slide>()
  const currentSlideData = ref<RowData[]>([])

  return {
    slides,
    isPreview,
    currentSlide,
    currentSlideData
  }
})
