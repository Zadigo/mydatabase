import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

import type { BlockItem, BlockItemData, Sheet, Slide, SlideData } from 'src/types'
import type { BlockRequestData } from 'src/utils'

export const useSlides = defineStore('slides', () => {
  const slides = ref<Slide[]>([])
  const currentSlide = ref<Slide>()

  const currentSlideData = ref<SlideData>()
  const currentSheet = ref<Sheet>()

  // Block level
  const currentBlock = ref<BlockItem>()
  const currentBlockData = ref<BlockItemData>()

  const blockRequestData = ref<BlockRequestData>({
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
  })

  /**
   * Checks if user needs to click save either at the slide
   * level or at the block level
   */
  const requiresSave = computed(() => {
    return false
  })

  /**
   * Checks if a block was selected in a slide 
   */
  const blockSelected = computed(() => {
    // Checks if a block was selected in a slide
    if (currentBlock.value) {
      return true
    } else {
      return false
    }
  })

  /**
   * Checks if the current slide has blocks 
   */
  const hasActiveBlocks = computed(() => {
    return currentSlide.value.blocks.length > 0
  })

  /**
   * Checks if data is currently loaded
   * on the slide level
   */
  const slideHasData = computed(() => {
    if (currentSlideData.value) {
      return Object.keys(currentSlideData.value).length > 0
    } else {
      return false
    }
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

  /**
   * The active sidebar component to use
   * when navigating the SlideView
   */
  const activeSidebarComponent = computed(() => {
    const component = 'default-slide-sidebar'

    switch (currentBlock.value.component) {
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
  })

  function loadFromCache() {
    // TODO: When the user lands directly on /slide/2 for example
    // the session does not have "slides" or "connections" in the
    // cache and we need to reload from the backend

    // Reload some data from the cache
    if (slides.value.length === 0) {
      slides.value = $session.retrieve('slides') || []
    }
  }

  /**
   * Set the current values for the
   * in the requestData for the current
   * selected block
   */
  function setCurrentBlockRequestData() {
    if (blockSelected.value) {
      Object.keys(blockRequestData.value).forEach((key) => {
        blockRequestData.value[key] = currentBlock.value[key]
      })
    }
  }

  /**
   * Sets currentSlide to the slide
   * matching the ID in slides
   * 
   * @param id 
   */
  function setCurrentSlide(id: string | number | null) {
    loadFromCache()

    if (currentSlide.value) {
      if (id) {
        currentSlide.value = slides.value.find(x => x.id === id * 1)
      }
    }
  }

  /**
   * Sets the current slide data 
   */
  function setCurrentSlideData(slideId: string | number | null, data) {
    currentSlideData.value = data.results
    $session.create(slideId, data.results)
  }

  /**
   * Reset the modifications made
   * to the blockRequestData
   */
  function resetBlockRequestData() {
    // slideRequiresSave = false
    // blockRequiresSave = false
    blockRequestData.value = {
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

  return {
    slides,
    currentSlide,
    currentSlideData,
    currentSheet,
    currentBlock,
    currentBlockData,
    blockRequestData,
    requiresSave,
    blockSelected,
    hasActiveBlocks,
    slideHasData,
    blockHasData,
    dataToUse,
    activeSidebarComponent,
    loadFromCache,
    setCurrentBlockRequestData,
    setCurrentSlide,
    setCurrentSlideData,
    resetBlockRequestData
  }
})
