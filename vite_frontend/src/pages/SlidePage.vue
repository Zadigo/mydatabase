<template>
  <section id="slide">
    <div class="row my-5">
      <div class="col-3">
        <div class="card shadow-sm">
          <div class="card-body">
            <!-- <v-breadcrumbs :items="[{ title: 'Slide', href: 'slide_view' }, { title: 'Block' }]">
              <template v-slot:divider>
                <v-icon icon="mdi-chevron-right"></v-icon>
              </template>
            </v-breadcrumbs> -->

            <component :is="activeSidebarComponent" />
          </div>
        </div>
      </div>

      <section class="col-9">
        <div class="row">
          <!-- Header -->
          <header id="block-selection" class="col-12">
            <div class="card shadow-sm mb-5">
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-center">
                  <div class="d-flex justify-content-end w-100 gap-2">
                    <button v-for="blockType in blockTypes" :key="blockType.name" type="button" class="btn btn-info shadow-none btn-rounded" rounded @click="handleAddBlock(blockType)">
                      <IconBase :icon="`${blockType.icon}`" />
                    </button>
                  </div>

                  <div class="d-flex justify-content-end gap-2">
                    <button type="button" class="btn btn-rounded btn-dark d-flex inline-flex ms-3 shadow-none align-items-center" rounded>
                      <IconBase icon="fa-solid:eye" class="me-2" />
                      Publish
                    </button>

                    <div v-if="currentSlide">
                      <router-link :to="{ name: 'page_preview', params: { id: currentSlide.slide_id } }" elevation="0" color="info" rounded>
                        <IconBase name="fa-solid:eye" class="me-2" />
                        Preview
                      </router-link>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </header>

          <!-- Blocks -->
          <section id="blocks" class="col-12">
            <div v-if="currentSlide && slidesStore.hasActiveBlocks">
              <component :is="block.component" v-for="(block, i) in currentSlide.blocks" :key="block.block_id" :class="{ 'mb-2': i >= 0 }" :block-details="block" :is-selected="checkIsSelected(block)" @block-selected="handleBlockSelection" />
            </div>

            <div v-else class="text-center text-body-tertiary">
              <div class="row">
                <div class="col-md-12">
                  <div class="card shadow-sm">
                    <div class="card-body">
                      <IconBase icon="fa-solid:home" class="fa-6x" />
                      <p class="my-3">
                        Lorem ipsum dolor sit amet consectetur adipisicing elit.
                        Enim cupiditate aliquid vero fuga rem suscipit ducimus in
                        exercitationem architecto, dolorem, sint libero quae hic quidem
                        reiciendis rerum. Natus, voluptas aliquam!
                      </p>

                      <button type="button" class="btn btn-info btn-lg btn-rounded shadow-none" @click="showBlocksModal=true">
                        Add your first block
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>
        </div>
      </section>
    </div>

    <!-- Modals -->
    <!-- <v-dialog v-model="showBlocksModal" width="600">
      <v-card title="Blocks">
        <v-card-text>
          <div class="row gap-1 gy-2">
            <div v-for="blockType in blockTypes" :key="blockType.name" class="col-3">
              <v-sheet :elevation="1" height="auto" width="auto" rounded @click="handleAddBlock(blockType)">
                <font-awesome-icon :icon="['fas', `${blockType.icon}`]" class="fa-3x" />
              </v-sheet>
            </div>
          </div>
        </v-card-text>
      </v-card>
    </v-dialog> -->
  </section>
</template>

<script setup lang="ts">
import { useStorage } from '@vueuse/core'
import { storeToRefs } from 'pinia'
import { api } from 'src/plugins'
import { useDatasource } from 'src/stores/datasources'
import { useSlides } from 'src/stores/slides'
import { computed, onMounted, ref, type Component } from 'vue'
import { useRoute } from 'vue-router'

import { type DeafaultComponentTypes } from 'src/data'
import type { BlockItem, DataSource, DataSourceDataApiResponse, ExtendedRouteParamsGeneric } from 'src/types'
import { useDatasourceComposable } from '@/composables/datasource'

// import DefaultSlideSidebar from 'src/components/sidebar/DefaultSlideSidebar.vue'

type BlockSelection = Record<string, boolean>

type BlockType = {
  name: string
  component: Component | (() => Promise<{ default: Component }>)
  // sidebar: Component | (() => Promise<{ default: Component }>)
  shortname: DeafaultComponentTypes
  icon: string
}

const { id: slideId } = useRoute().params as ExtendedRouteParamsGeneric

const cachedDatasources = useStorage<DataSource[]>('dataSources', [])

const slidesStore = useSlides()
const { currentSlide, currentBlock } = storeToRefs(slidesStore)

const datasourceStore = useDatasource()
const { getConnections } = useDatasourceComposable()

const showBlocksModal = ref<boolean>(false)
const blockSelections = ref<BlockSelection>({})

const blockTypes: BlockType[] = [
  {
    name: 'Table',
    component: () => import('@/components/slide/blocks/TableBlock.vue'),
    shortname: 'table-block',
    icon: 'fa-solid:table'
  },
  {
    name: 'Calendar',
    component: () => import('@/components/slide/blocks/TableBlock.vue'),
    shortname: 'calendar-block',
    icon: 'fa-solid:calendar'
  },
  {
    name: 'Chart',
    component: () => import('@/components/slide/blocks/ChartBlock.vue'),
    shortname: 'chart-block',
    icon: 'fa-solid:chart-line'
  },
  {
    name: 'Grid',
    component: () => import('@/components/slide/blocks/GridByTwoBlock.vue'),
    shortname: 'grid-2-block',
    icon: 'fa6-solid:table-cells-large'
  }
]

/**
 * The active sidebar component to use
 * when navigating the SlideView
 */
const activeSidebarComponent = computed(() => {
  let component: Component | (() => Promise<{ default: Component }>) = () => import('src/components/slide/sidebars/DefaultSlideSidebar.vue')

  if (currentBlock.value) {
    switch (currentBlock.value.component) {
      case 'table-block':
        component = () => import('src/components/slide/sidebars/DefaultSlideSidebar.vue')
        break

      case 'chart-block':
        component = () => import('src/components/slide/sidebars/DefaultSlideSidebar.vue')
        break

      default:
        break
    }
  }

  return component
})

console.log('activeSidebarComponent', activeSidebarComponent.value)

/**
 * TODO:
 */
async function handleAddBlock(blockType: BlockType) {
  // Creates a new block for the slide
  try {
    const path = `/api/v1/sheets/pages/${pageStore.currentPage.page_id}/blocks/create`
    const response = await api.post(path, {
      name: null,
      component: blockType.component,
      conditions: { filters: [] }
    })

    currentPage.blocks.push(response.data)
    this.$session.create('pages', this.pageStore.pages)
    this.showBlocksModal = false
  } catch (e) {
    console.error(e)
  }
}

/**
 * TODO:
 */
// async function handleUpdateSlide() {
//   Changes the source for the given page
//   try {
//     const path = `slides/${this.currentSlide.slide_id}/blocks/${this.currentBlock.block_id}/update`
//     // this.blockRequestData.block_data_source = blockId
//     const response = await this.$http.post(path, this.pageRequestData)
//     this.currentSlide = response.data
//     await this.getBlockData((data) => {
//       data
//     })
//   } catch (e) {
//     console.log(e)
//   }
// }

/**
 * TODO:
 */
// async function handleUpdateBlock() {}

/**
 * Gets the data for the current slide
 */
async function getSlideData() {
  try {
    if (currentSlide.value && currentSlide.value.slide_data_source) {
      const response = await api.get<DataSourceDataApiResponse>(`/api/v1/datasources/${currentSlide.value.slide_data_source.data_source_id}`)
      slidesStore.setCurrentSlideData(currentSlide.value.slide_data_source.data_source_id, response.data)
    } else {
      console.log('Slide does not have a datasource - will be using block data source')
    }
  } catch (e) {
    console.log(e)
  }
}

/**
 * Handle the selection state for each block
 */
function handleBlockSelection(blockDetails: BlockItem) {
  Object.keys(blockSelections.value).forEach((key) => {
    if (key !== blockDetails.block_id) {
      blockSelections.value[key] = false
    }
  })

  const state = blockSelections.value[blockDetails.block_id]
  blockSelections.value[blockDetails.block_id] = !state

  // Overall, if a block is selected, then set the currentBlock
  // to be the one that is being selected otherwise, it should
  // just be an empty object
  const hasSelection = Object.values(blockSelections.value).some(x => x)
  if (hasSelection) {
    currentBlock.value = blockDetails
  } else {
    currentBlock.value = undefined
  }
  slidesStore.setCurrentBlockRequestData()
}

/**
 *
 */
function checkIsSelected(blockDetails: BlockItem) {
  // Returns the selection state for the given block
  return blockSelections.value[blockDetails.block_id]
}

slidesStore.setCurrentSlide(slideId)

onMounted(async () => {
  await getSlideData()
  datasourceStore.setCurrentDatasource(currentSlide.value)

  if (cachedDatasources.value.length === 0) {
    await getConnections((data) => {
      cachedDatasources.value = data
    })
  }

  if (currentSlide.value) {
    // Container that manages the selection state
    // for each block of the slide
    currentSlide.value.blocks.forEach((block) => {
      blockSelections.value[block.block_id] = false
    })
  }
})
</script>
