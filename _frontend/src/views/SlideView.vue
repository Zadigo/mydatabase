<template>
  <section id="slide">
    <div class="container">
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
            Blocks here
            <!-- <component :is="block.component" v-for="(block, i) in currentSlide.blocks" :key="block.block_id" :class="{ 'mb-2': i >= 0 }" :block-details="block" :is-selected="checkIsSelected(block)" @block-selected="handleBlockSelection" /> -->
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

<script>
import _ from 'lodash'
import { ref } from 'vue'
import { storeToRefs } from 'pinia'
import { mapActions } from 'pinia'
import { useSlides } from '@/store/slides'
import { useConnections } from '@/store/connections'
import { useSheetsComposable } from '@/composables/page'

import BaseButton from '../layouts/bootstrap/buttons/BaseButton.vue'
import BaseCard from '../layouts/bootstrap/cards/BaseCard.vue'
// import ChartBlock from '../components/blocks/ChartBlock.vue'
// import GridByTwoBlock from '../components/blocks/GridByTwoBlock.vue'
// import TableBlock from '../components/blocks/TableBlock.vue'

export default {
  name: 'SlideView',
  components: {
    BaseButton,
    BaseCard,
    // ChartBlock,
    // GridByTwoBlock,
    // TableBlock
  },
  beforeRouteEnter (to, from, next) {
    next(vm => {
      vm.setCurrentSlide(to.params.id)
      vm.getSlideData()
      vm.connectionsStore.loadFromCache()
      vm.connectionsStore.setCurrentConnection(vm.currentSlide.slide_data_source)
    })
  },
  setup () {
    const slidesStore = useSlides()
    const { slides, currentSlide, currentBlock } = storeToRefs(slidesStore)
    const connectionsStore = useConnections()
    const showBlocksModal = ref(false)
    const { getConnections } = useSheetsComposable()
    const blockSelections = ref({})
    
    return {
      currentSlide,
      currentBlock,
      showBlocksModal,
      slides,
      slidesStore,
      connectionsStore,
      getConnections,
      blockSelections
    }
  },
  data () {
    return {
      blockTypes: [
        {
          name: 'Table',
          component: 'table-block',
          icon: 'table'
        },
        {
          name: 'Calendar',
          component: 'calendar-block',
          icon: 'calendar'
        },
        {
          name: 'Chart',
          component: 'chart-block',
          icon: 'chart-simple'
        },
        {
          name: 'Grid',
          component: 'grid-by-two-block',
          icon: 'table-cells-large'
        }
      ]
    }
  },
  created () {
    if (!this.$session.exists('connections')) {
      this.getConnections((data) => {
        this.$session.create('connections', data)
      })
    }

    // Container that manages the selection state
    // for each block of the slide
    _.forEach(this.currentSlide.blocks, (block) => {
      this.blockSelections[block.block_id] = false
    })
  },
  methods: {
    ...mapActions(useSlides, ['setCurrentSlide', 'setCurrentSlideData']),
    async handleAddBlock (blockType) {
      // Creates a new block for the slide
      try {
        const path = `sheets/pages/${this.pageStore.currentPage.page_id}/blocks/create`
        const response = await this.$http.post(path, {
          name: null,
          component: blockType.component,
          conditions: { filters: [] }
        })

        this.currentPage.blocks.push(response.data)
        this.$session.create('pages', this.pageStore.pages)
        this.showBlocksModal = false
      } catch (e) {
        console.error(e)
      }
    },
    async handleUpdateSlide () {
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
    },
    async handleUpdateBlock () {

    },
    async getSlideData () {
      // Gets the data for the current slide
      try {
        const response = await this.$http.get(`sheets/${this.currentSlide.slide_data_source}`)
        this.setCurrentSlideData(this.currentSlide.slide_data_source, response.data)
      } catch (e) {
        console.log(e)
      }
    },
    handleBlockSelection (blockDetails) {
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
    },
    checkIsSelected (blockDetails) {
      // Returns the selection state for the given block
      return this.blockSelections[blockDetails.block_id]
    }
  }
}
</script>
