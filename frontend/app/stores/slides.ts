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
    slides.value = [
      { id: 1, name: 'Introduction to Vue.js' },
      { id: 2, name: 'Advanced Vue.js Techniques' },
      { id: 3, name: 'State Management with Vuex' },
      { id: 4, name: 'Building Reusable Components' },
      { id: 5, name: 'Vue Router Basics' }
    ]
  }

  /**
   * Current slide
   */

  const { id } = useRoute().params as { id: string }
  const activeSlide = computed(() => {
    if (id) {
      return slides.value.find(slide => slide.id.toString() === id) || null
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
