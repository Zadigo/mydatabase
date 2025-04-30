<template>
  <section id="slide">
    <div class="row">
      <div class="col-3">
        <base-card class="shadow-sm">
          <template #body>
            <!-- <v-breadcrumbs :items="[{ title: 'Slide', href: 'slide_view' }, { title: 'Block' }]">
              <template v-slot:divider>
                <v-icon icon="mdi-chevron-right"></v-icon>
              </template>
            </v-breadcrumbs> -->

            <component :is="activeSidebarComponent" />
          </template>
        </base-card>
      </div>
      
      <section class="col-9">
        <div class="row">
          <!-- Header -->
          <section id="block-selection" class="col-12">
            <base-card class="shadow-sm mb-5">
              <template #body>
                <div class="d-flex justify-content-between align-items-center">
                  <div class="d-flex justify-content-start gap-2">
                    <base-button v-for="blockType in blockTypes" :key="blockType.name" color="light" rounded @click="handleAddBlock(blockType)">
                      <font-awesome-icon :icon="['fas', `${blockType.icon}`]" />
                    </base-button>
                  </div>
                  
                  <div class="d-flex justify-content-end gap-2">
                    <!-- <v-btn elevation="0" color="secondary" rounded>
                      <font-awesome-icon :icon="['fas', 'eye']" class="me-2" />
                      Publish
                    </v-btn> -->
  
                    <v-btn :to="{ name: 'page_preview_view', params: { id: currentSlide.slide_id } }" elevation="0" color="info" rounded>
                      <font-awesome-icon :icon="['fas', 'eye']" class="me-2" />
                      Preview
                    </v-btn>
                  </div>
                </div>
              </template>
            </base-card>
          </section>
          
          <!-- Blocks -->
          <section id="blocks" class="col-12">
            <div v-if="slidesStore.hasActiveBlocks">
              <component :is="block.component" v-for="(block, i) in currentSlide.blocks" :key="block.block_id" :class="{ 'mb-2': i >= 0 }" :block-details="block" :is-selected="checkIsSelected(block)" @block-selected="handleBlockSelection" />
            </div>
  
            <div v-else class="text-center text-body-tertiary">
              <div class="row">
                <div class="col-md-6 offset-md-3">
                  <font-awesome-icon :icon="['fas', 'home']" class="fa-6x" />
                  <p class="my-3">
                    Lorem ipsum dolor sit amet consectetur adipisicing elit. 
                    Enim cupiditate aliquid vero fuga rem suscipit ducimus in 
                    exercitationem architecto, dolorem, sint libero quae hic quidem 
                    reiciendis rerum. Natus, voluptas aliquam!
                  </p>
                  
                  <v-btn color="primary" variant="tonal" size="x-large" rounded @click="showBlocksModal = true">
                    Add your first block
                  </v-btn>
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
import { onMounted, ref, type Component } from 'vue'
import { storeToRefs } from 'pinia'
import { mapActions } from 'pinia'
import { useSlides } from 'src/stores/slides'
import { useConnections } from 'src/stores/connections'
import { useSheetsComposable } from 'src/composables/page'
import { useRoute } from 'vue-router'
import { type DeafaultComponentTypes } from 'src/data'

import { onBeforeMount } from 'vue'
import { api } from 'src/boot/axios'
import { DataSource, DataSourceDataApiResponse } from 'src/types'
import { useStorage } from '@vueuse/core'

// import DefaultSlideSidebar from 'src/components/sidebar/DefaultSlideSidebar.vue'

type BlockSelection = Record<string, boolean>

type BlockType = {
  name: string
  component: Component | (() => Promise<{ default: Component }>)
  // sidebar: Component | (() => Promise<{ default: Component }>)
  shortname: DeafaultComponentTypes
  icon: string
}

const connections = useStorage('connections', [])
const route = useRoute()
const slidesStore = useSlides()
const { slides, currentSlide, currentBlock, activeSidebarComponent } = storeToRefs(slidesStore)

const connectionsStore = useConnections()
const { getConnections } = useSheetsComposable()

const showBlocksModal = ref<boolean>(false)
const blockSelections = ref<BlockSelection>({})

const blockTypes: BlockType[] = [
  {
    name: 'Table',
    component: () => import('src/components/blocks/TableBlock.vue'),
    shortname: 'table-block',
    icon: 'table'
  },
  {
    name: 'Calendar',
    component: () => import('src/components/blocks/TableBlock.vue'),
    shortname: 'calendar-block',
    icon: 'calendar'
  },
  {
    name: 'Chart',
    component: () => import('src/components/blocks/ChartBlock.vue'),
    shortname: 'chart-block',
    icon: 'chart-simple'
  },
  {
    name: 'Grid',
    component: () => import('src/components/blocks/GridByTwoBlock.vue'),
    shortname: 'grid-2-block',
    icon: 'table-cells-large'
  }
]

/**
 * 
 */
async function handleAddBlock (blockType: DeafaultComponentTypes) {
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
 * 
 */
async function handleUpdateSlide () {
  // Changes the source for the given page
  // try {
  //   const path = `slides/${this.currentSlide.slide_id}/blocks/${this.currentBlock.block_id}/update`
  //   // this.blockRequestData.block_data_source = blockId
  //   const response = await this.$http.post(path, this.pageRequestData)
  //   this.currentSlide = response.data
  //   await this.getBlockData((data) => {
  //     data
  //   })
  // } catch (e) {
  //   console.log(e)
  // }
}

/**
 * 
 */
async function handleUpdateBlock () {

}

/**
 * 
 */
async function getSlideData () {
  // Gets the data for the current slide
  try {
    if (currentSlide.value) {
      const response = await api.get<DataSourceDataApiResponse>(`/api/v1/sheets/${currentSlide.value.slide_data_source}`)
      slidesStore.setCurrentSlideData(currentSlide.value.slide_data_source.data_source_id, response.data)
    }
  } catch (e) {
    console.log(e)
  }
}

/**
 * 
 */
function handleBlockSelection (blockDetails) {
  // Handle the selection state for each block
  Object.keys(this.blockSelections).forEach((key) => {
    if (key !== blockDetails.block_id) {
      this.blockSelections[key] = false
    }
  })

  const state = this.blockSelections[blockDetails.block_id]
  this.blockSelections[blockDetails.block_id] = !state
  
  // Overall, if a block is selected, then set the currentBlock
  // to be the one that is being selected otherwise, it should
  // just be an empty object
  const hasSelection = Object.values(this.blockSelections).some(x => x === true)
  if (hasSelection) {
    this.slidesStore.currentBlock = blockDetails
  } else {
    this.slidesStore.currentBlock = {}
  }
  this.slidesStore.setCurrentBlockRequestData()
}

/**
 * 
 */
function checkIsSelected (blockDetails) {
  // Returns the selection state for the given block
  return this.blockSelections[blockDetails.block_id]
}

onBeforeMount(async () => {
  console.log('SlideView before route enter (1)')
  slidesStore.setCurrentSlide(route.params.id)
  
  await getSlideData()

  connectionsStore.setCurrentConnection(slidesStore.currentSlide?.slide_data_source)
})

onMounted(async () => {
  if (!connections.value) {
    await getConnections((data) => {
      connections.value = data
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
