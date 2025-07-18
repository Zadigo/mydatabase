import type { BlockType } from '~/data/constants'
import type { Block } from '~/types'

export function useBlocks() {
  const store = useSlideStore()
  const { activeSlide } = storeToRefs(store)
  
  const blocks = computed(() => activeSlide.value?.blocks || [])
  const hasBlocks = computed(() => blocks.value.length > 0)
  
  function create(blockType: BlockType) {
    // const path = `sheets/pages/${this.pageStore.currentPage.page_id}/blocks/create`
    const newBlock = {
      name: null,
      component: blockType.component,
      conditions: { filters: [] }
    }
  }

  const showCreateModal = ref<boolean>(false)

  const dynamicComponents = {
    'table-component': () => import('~/components/blocks/Table.vue'),
    'chart-component': () => import('~/components/blocks/Chart.vue'),
    'grid-component': () => import('~/components/blocks/GridByTwo.vue')
  }
  
  return {
    dynamicComponents,
    /**
     * Creates a new block of the specified type
     * @param blockType The type of block to create
     */
    create,
    /**
     * Returns the blocks of the active slide
     */
    blocks,
    /**
     * Returns whether the active slide has blocks
     */
    hasBlocks,
    /**
     * Returns whether the create modal is shown
     */
    showCreateModal,
  }
}

/**
 * A composable for managing blocks in slides
 */
export function useBlock(block: Block) {
  const { blocks, hasBlocks } = useBlocks()

   

  return {
    /**
     * Returns whether the active slide has blocks
     */
    hasBlocks,
    /**
     * Returns the blocks of the active slide
     */
    blocks
  }
}
