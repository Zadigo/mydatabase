import { defineAsyncComponent } from 'vue'

import type { defineAsyncComponent as DefineAsyncComponent } from 'vue'
import type { BlockType, BlockTypeNames } from '~/data/constants'
import type { Block } from '~/types'
import type { TableColumn } from '@nuxt/ui'

/**
 * A composable to handle blocks in slides
 */
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

  const dynamicComponents: Record<BlockTypeNames, ReturnType<typeof DefineAsyncComponent>> = {
    'table-block': defineAsyncComponent(() => import('~/components/blocks/Table.vue')),
    'chart-block': defineAsyncComponent(() => import('~/components/blocks/Chart.vue')),
    'grid-by-two-block': defineAsyncComponent(() => import('~/components/blocks/GridByTwo.vue'))
  }

  /**
   * Selection
   */
  const currentSelection = ref<Block>()
  
  return {
    /**
     * Current block selected by the user
     */
    currentSelection,
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
 * A composable to handle block data and operations
 */
export function useBlock<D, T extends Record<string, unknown>[]>(block: Block, slideDatasource: Record<string, unknown> | null = null) {
  const activeBlock = toRef(block)

  const datasource = computed(() => activeBlock.value.data_source || slideDatasource || null)
  const activeData = ref<{ columns: TableColumn<D>[], results: T }[]>([])

  async function loadData() {
    // Transform to useAsyncData
    activeData.value = {
      columns: [
        {
          accessorKey: 'id',
          header: 'ID',
        },
        {
          accessorKey: 'name',
          header: 'Name'
        }
      ],
      results: [
        {
          id: '1',
          name: 'Kendall Jenner'
        },
        {
          id: '2',
          name: 'Kylie Jenner'
        },
        {
          id: '3',
          name: 'Kim Kardashian'
        },
        {
          id: '4',
          name: 'Kourtney Kardashian'
        },
        {
          id: '5',
          name: 'Khloé Kardashian'
        }
      ]
    }
  }

  onBeforeMount(async () => {
    await loadData()
  })

  return {
    loadData,
    datasource,
    activeData
  }
}

/**
 * 
 * @param block The block to use
 * @param slideDatasource The datasource of the slide, if any
 */
export function useTableBlock(block: Block, slideDatasource: Record<string, unknown> | null = null) {
  const activeBlock = toRef(block)
  const { activeData, datasource } = useBlock(block, slideDatasource)

  /**
   * Function used to persanlize the header for the
   * data table in the block
   * @reference https://ui.nuxt.com/components/table
   */
  function createSortableButton() {}

  const currentBlockPermissions = reactivePick(activeBlock.value, 'allow_record_creation', 'allow_record_creation', 'allow_record_creation', 'allow_record_search', 'allow_record_update', 'active')

  onMounted(() => {
    // TODO: Run all th necessary oprations on the the data
    // to prapare it to be integrated into the table
  })

  return {
    /**
     * Reactive object containing the permissions of the block
     * @property allow_record_creation Whether the block allows record creation
     * @property allow_record_deletion Whether the block allows record deletion
     * @property allow_record_search Whether the block allows record search
     * @property allow_record_update Whether the block allows record update
     * @property active Whether the block is active
     */
    currentBlockPermissions,
    activeData,
    datasource
  }
}


type BlockPermissions = Pick<Block, 'allow_record_creation' | 'allow_record_update' | 'allow_record_search' | 'active'>

export function useBlockPermissions(permissions: BlockPermissions) {
  const currentBlockPermissions = reactive(permissions)

  const [showSearchPermissionsModal, toggleSearchPermissionsModal] = useToggle()
  const [showCreatePermissionsModal, toggleCreatePermissionsModal] = useToggle()

  return {
    currentBlockPermissions,
    showSearchPermissionsModal,
    showCreatePermissionsModal,
    toggleSearchPermissionsModal,
    toggleCreatePermissionsModal
  }
  
}
