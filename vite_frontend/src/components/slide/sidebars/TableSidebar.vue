<template>
  <div id="inner-sidebar" class="my-1">
    <!-- Sheets -->
    <!-- <v-select id="sheet-selection" v-model="blockRequestData.block_data_source" :items="connections" item-title="name" item-value="sheet_id" placeholder="Select block data source" variant="outlined" clearable hide-details @update:model-value="handleBlockUpdate" />

    <div v-if="slideHasData" class="mt-2 alert alert-warning">
      Block uses page data source
    </div>

    <div class="my-4">
      <v-switch v-model="blockRequestData.allow_record_creation" label="Record creation" inset hide-details @update:model-value="handleBlockUpdate" />
      <v-switch v-model="blockRequestData.allow_record_update" label="Record updates" inset hide-details @update:model-value="handleBlockUpdate" />
    </div> -->

    <!-- Filters -->
    <!-- <h3 class="h6">
      Filters
    </h3>

    <active-filter v-for="item in currentBlockToEdit.conditions.filters" :key="item.id" :filter-data="item" />

    <button type="button" class="mt-1 btn btn-primary" variant="tonal" density="compact" rounded @click="showDataFiltersModal = true">
      Add data filters
    </button> -->

    <hr class="my-3">

    <!-- Advanced -->
    <h3 class="h6">
      Advanced
    </h3>

    <hr class="my-3">

    <!-- Group -->
    <h3 class="h6">
      Group
    </h3>

    <!-- <button class="btn btn-primary" rounded block @click="handleBlockDeletion">
      Delete
    </button> -->

    <!-- Modals -->
    <!-- <teleport to="body">
      <v-dialog v-model="showDataFiltersModal" width="800">
        <v-card>
          <v-card-text>
            <h2 class="h4 mb-4">
              Create data filters
            </h2>

            <template v-for="(dataFilter, i) in blockRequestData.conditions.filters" :key="i">
              <union-filter v-if="i > 0" :position="i" :filter-details="dataFilter" :is-data-filter="true" />
              <simple-filter v-else :position="i" :filter-details="dataFilter" :is-data-filter="true" />
            </template>

            <div class="row">
              <div class="col-12 mt-4 d-flex justify-content-start">
                <button variant="tonal" color="info" rounded @click="handleAddFilter">
                  Add filter
                </button>
              </div>
            </div>
          </v-card-text>

          <v-card-actions class="justify-content-end">
            <button @click="showDataFiltersModal = false">
              Cancel
            </button>

            <button variant="tonal" @click="handleBlockUpdate">
              Validate
            </button>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </teleport> -->
  </div>
</template>

<script setup lang="ts">
import { api } from '@/plugins'
import { useEditing } from '@/stores/editing'
import { storeToRefs } from 'pinia'
import { useDatasource } from 'src/stores/datasources'
import { useSlides } from 'src/stores/slides'
import { ref } from 'vue'

// import ActiveFilter from '../../components/filters/ActiveFilter.vue'
// import SimpleFilter from './filters/SimpleFilter.vue'
// import UnionFilter from './filters/UnionFilter.vue'

const editingStore = useEditing()
const { currentBlockToEdit, blockRequestData, slideHasData } = storeToRefs(editingStore)

const slidesStore = useSlides()
const { currentSlide, currentSlideData } = storeToRefs(slidesStore)

const showDataFiltersModal = ref<boolean>(false)

/**
 * Deletes a block from a given page
 */
// async function handleBlockDeletion() {
//   try {
//     if (currentSlide.value && currentBlockToEdit.value) {
//       const path = `slides/${currentSlide.value.slide_id}/blocks/${currentBlockToEdit.value.block_id}/delete`
//       await api.post(path)
//     }
//   } catch (e) {
//     console.log(e)
//   }
// }

// async function handleBlockUpdate() {
//   this.handleChangeBlockSource()
// }

/**
 * Changes the source for the given page
 */
// async function handleChangeBlockSource() {
//   try {
//     if (currentSlide.value && currentBlockToEdit.value) {
//       const path = `slides/${currentSlide.value.slide_id}/blocks/${currentBlockToEdit.value.block_id}/update`
//       const response = await api.post(path, pageRequestData.value)

//       slidesStore.currentBlockData = response.data
//     }
//   } catch (e) {
//     console.log(e)
//   }
// }

/**
 *
 */
// function handlePartialSave() {
//   showDataFiltersModal.value = false
// }

/**
 * Adds a new user filter
 */
// function handleAddFilter() {
//   blockRequestData.value.conditions.filters.push({
//     column: '',
//     operator: 'equals',
//     input_type: 'Input'
//   })
// }
</script>
