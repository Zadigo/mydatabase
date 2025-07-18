export * from './create'

export function useGetSlideData() {
  const store = useSlideStore()
  const { activeSlide } = storeToRefs(store)
  const activeData = ref<Record<string, unknown>[]>()

  async function retrieve() {
    // useAsyncData
    activeData.value = [
      {
        id: 1,
        name: 'Kendall Jenner'
      },
      {
        id: 2,
        name: 'Kylie Jenner'
      },
      {
        id: 3,
        name: 'Kim Kardashian'
      },
      {
        id: 4,
        name: 'Kourtney Kardashian'
      },
      {
        id: 5,
        name: 'Khloé Kardashian'
      }
    ]
  }

  onMounted(async () => {
    await retrieve()
  })

  return {
    /**
     * The current active data for the slide
     */
    activeData,
    /**
     * Returns the underlying data that the 
     * current slide is based on
     */
    retrieve
  }
}
