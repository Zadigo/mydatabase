import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

import type { BlockItemData, DataSourceDataApiResponse, RowData, Slide } from '../types'

export const useSlides = defineStore('slides', () => {
  const slides = ref<Slide[]>([])
  const currentSlide = ref<Slide>()

  const cachedSlidesData = ref<Record<string, RowData[]>>({})
  const currentSlideData = ref<RowData[]>([])

  // Block level
  const currentBlockData = ref<BlockItemData>()

  /**
   * Checks if user needs to click save either at the slide
   * level or at the block level
   */
  const requiresSave = computed(() => {
    return false
  })

  /**
   * Checks if the current slide has blocks
   */
  const hasActiveBlocks = computed(() => {
    if (currentSlide.value) {
      return currentSlide.value.blocks.length > 0
    } else {
      return false
    }
  })

  /**
   * Checks if data is currently loaded
   * on the slide level
   */
  const slideHasData = computed(() => {
    return currentSlideData.value.length > 0
  })

  /**
   * Checks if data is currently loaded
   * on the block level
   */
  const blockHasData = computed(() => {
    if (currentBlockData.value) {
      return Object.keys(currentBlockData.value).length > 0
    } else {
      return false
    }
  })

  /**
   * Returns either the slide level data
   * or the block level data
   */
  const dataToUse = computed(() => {
    if (blockHasData.value) {
      return currentBlockData.value
    }

    if (slideHasData.value) {
      return currentSlideData.value
    }

    return null
  })

  // function loadFromCache() {
  //   // TODO: When the user lands directly on /slide/2 for example
  //   // the session does not have "slides" or "connections" in the
  //   // cache and we need to reload from the backend

  //   // Reload some data from the cache
  //   if (slides.value.length === 0) {
  //     slides.value = $session.retrieve('slides') || []
  //   }
  // }

  /**
   * Sets currentSlide to the slide
   * matching the ID in slides
   *
   * @param slideId The ID of the slide to get
   */
  function setCurrentSlide(slideId: string | null) {
    if (slideId) {
      currentSlide.value = slides.value.find(x => x.slide_id === slideId)
      console.log('setCurrentSlide', currentSlide.value)
    }
  }

  /**
   * Sets the current slide data
   *
   * @param slideId
   * @param data
   */
  function setCurrentSlideData(slideId: string | number | null, data: DataSourceDataApiResponse) {
    currentSlideData.value = data.results

    if (slideId) {
      cachedSlidesData.value[slideId] = data.results
    }
  }

  return {
    slides,
    currentSlide,
    currentSlideData,
    currentBlockData,
    requiresSave,
    hasActiveBlocks,
    slideHasData,
    blockHasData,
    dataToUse,
    cachedSlidesData,

    setCurrentSlide,
    setCurrentSlideData
  }
})
