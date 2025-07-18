/**
 * A composable for managing blocks in slides
 */
export function useBlock() {
  const store = useSlideStore()
  const { activeSlide } = storeToRefs(store)

  const blocks = ref([])
  const blockConnection = ref({})

  function getBlocks() {
    // Simulate fetching blocks from an API or database
    blocks.value = activeSlide.value?.blocks || []
  }

  const hasBlocks = computed(() => {
    return blocks.value.length > 0
  })

  return {
    getBlocks,
    hasBlocks,
    blockConnection,
    blocks
  }
}
