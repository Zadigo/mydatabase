<template>
  <div id="inner-sidebar" class="my-1">
    <!-- Sheets -->
    <v-select id="sheet-selection" v-model="blockRequestData.block_data_source" :items="connections" item-title="name" item-value="sheet_id" placeholder="Select block data source" variant="outlined" clearable hide-details @update:model-value="handleBlockUpdate"></v-select>
    <div v-if="slideHasData" class="mt-2 alert alert-warning">
      Block uses page data source
    </div>

    <div class="my-4">
      <v-switch v-model="blockRequestData.allow_record_creation" label="Record creation" inset hide-details @update:model-value="handleBlockUpdate"></v-switch>
      <v-switch v-model="blockRequestData.allow_record_update" label="Record updates" inset hide-details @update:model-value="handleBlockUpdate"></v-switch>
    </div>

    <!-- Filters -->
    <h3 class="h6">Filters</h3>
    <active-filter v-for="item in currentBlock.conditions.filters" :key="item.id" :filter-data="item" />
    
    <v-btn class="mt-1" variant="tonal" density="compact" rounded @click="showDataFiltersModal = true">
      Add data filters
    </v-btn>

    <hr class="my-3">

    <!-- Advanced -->
    <h3 class="h6">Advanced</h3>

    <hr class="my-3">

    <!-- Group -->
    <h3 class="h6">Group</h3>

    <v-btn color="danger" variant="tonal" rounded block @click="handleBlockDeletion">Delete</v-btn>

    <!-- Modals -->
    <teleport to="body">
      <v-dialog v-model="showDataFiltersModal" width="800">
        <v-card>
          <v-card-text>
            <h2 class="h4 mb-4">Create data filters</h2>

            <template v-for="(dataFilter, i) in blockRequestData.conditions.filters" :key="i">
              <union-filter v-if="i > 0" :position="i" :filter-details="dataFilter" :is-data-filter="true" />
              <simple-filter v-else :position="i" :filter-details="dataFilter" :is-data-filter="true" />
            </template>

            <div class="row">
              <div class="col-12 mt-4 d-flex justify-content-start">
                <v-btn variant="tonal" color="info" rounded @click="handleAddFilter">
                  Add filter
                </v-btn>
              </div>
            </div>
          </v-card-text>

          <v-card-actions class="justify-content-end">
            <v-btn @click="showDataFiltersModal = false">Cancel</v-btn>
            <v-btn variant="tonal" @click="handleBlockUpdate">Validate</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </teleport>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useSlides } from '@/store/slides'
import { storeToRefs, mapState } from 'pinia'
import { useColumnFilters } from '@/composables/page'
import { useSheetsComposable } from '@/composables/page'
import { useConnections } from '@/store/connections'

import ActiveFilter from '../../components/filters/ActiveFilter.vue'
import SimpleFilter from './filters/SimpleFilter.vue'
import UnionFilter from './filters/UnionFilter.vue'

export default {
  name: 'TableSidebar',
  components: {
    ActiveFilter,
    SimpleFilter,
    UnionFilter
  },
  setup () {
    const slidesStore = useSlides()
    const { currentBlock, currentSlide, blockRequestData } = storeToRefs(slidesStore)
    const { defaultOperators, defaultColumnInputs } = useColumnFilters()
    const { getConnections, getSheetData, getBlockData } = useSheetsComposable()
    const connectionsStore = useConnections()
    const { connections, currentConnection } = storeToRefs(connectionsStore)
    const showDataFiltersModal = ref(false)
    // const blockRequestData = ref({
    //   name: null,
    //   allow_record_creation: false,
    //   allow_record_updates: false,
    //   block_data_source: null,
    //   search_columns: [],
    //   user_filters: [],
    //   active: true,
    //   conditions: {
    //     filters: [],
    //     columns_visibility: []
    //   }
    // })

    return {
      blockRequestData,
      connections,
      currentConnection,
      currentSlide,
      currentBlock,
      defaultOperators,
      defaultColumnInputs,
      showDataFiltersModal,
      slidesStore,
      getBlockData,
      getConnections,
      getSheetData
    }
  },
  computed: {
    ...mapState(useSlides, ['slideHasData'])
  },
  methods: {
    async handleBlockDeletion () {
      // Deletes a block from a given page
      try {
        const path = `slides/${this.currentSlide.slide_id}/blocks/${this.currentBlock.block_id}/delete`
        const response = await this.$http.post(path)
        this.currentSlide.blocks = response.data.blocks
        this.$session.create('slides', this.slidesStore.slides)
      } catch (e) {
        console.log(e)
      }
    },
    async handleBlockUpdate () {
      // this.handleChangeBlockSource()
    },
    async handleChangeBlockSource () {
      // Changes the source for the given page
      // try {
      //   const path = `slides/${this.currentSlide.slide_id}/blocks/${this.currentBlock.block_id}/update`
      //   // this.blockRequestData.block_data_source = blockId
      //   const response = await this.$http.post(path, this.pageRequestData)
      //   this.slidesStore.currentBlockData = response.data
      // } catch (e) {
      //   console.log(e)
      // }
    },
    handlePartialSave () {
      this.slidesStore.blockRequiresSave = true
      this.showDataFiltersModal = false
    },
    handleAddFilter () {
      // Adds a new user filter
      this.blockRequestData.conditions.filters.push({
        column: null,
        operator: 'equals',
        input_type: 'Input'
      })
    }
  }
}
</script>
