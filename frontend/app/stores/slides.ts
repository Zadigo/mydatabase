import { slidesFixture } from '~/data/fixtures'

import type { Slide } from '~/types'

export const useSlideStore = defineStore('slides', () => {
  /**
   * Slides
   */

  const slides = ref<Slide[]>([])
  const search = ref<string>('')
  
  const { last } = useRefHistory(search, { capacity: 10 }) 
   
  const searched = computed(() => {
    if (!search.value || search.value.trim() === '') {
      return slides.value
    } else {
      return slides.value.filter(slide => slide.name.toLowerCase().includes(search.value.toLowerCase()))
    }
  })

  async function getSlides() {
    // Simulate fetching slides from an API or database
    slides.value = slidesFixture
  }

  /**
   * Current slide
   */

  const { id } = useRoute().params as { id: string }

  console.log(id)
  
  const activeSlide = computed(() => {
    if (id) {
      return slides.value.find(slide => slide.slide_id.toString() === id) || null
    } else {
      return null
    }
  })

  return {
    slides,
    search,
    searched,
    lastSearch: last,
    /**
     * Returns the current slide being viewed based 
     * on the route parameter
     */
    activeSlide,
    getSlides
  }
})
