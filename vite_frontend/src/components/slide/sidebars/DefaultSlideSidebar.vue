<template>
  <div id="inner-sidebar" class="my-1">
    <input v-model="blockRequestData.name" variant="outlined" elevation="0" placeholder="Slide name" />
    <v-select id="sheet-selection" v-model="blockRequestData.slide_data_source" :items="connections" item-title="name" item-value="sheet_id" placeholder="Select sheet" variant="outlined" hide-details @update:model-value="handleChangePageSource" />

    <!-- Columns -->
    <div class="mt-5">
      <h2 class="h6">
        Columns
      </h2>

      <div v-if="currentConnection" class="list-group">
        <div v-for="column in currentConnection.columns" :key="column.name" class="list-group-item list-group-item-action p-3 d-block">
          <span class="fw-bold">
            {{ column }}
          </span>

          <div class="mt-2">
            <button class="me-1 btn btn-light btn-sm" @click="handleChangeColumnSetting(column)">
              <IconBase icon="fa-solid:cog" />
            </button>

            <button class=" btn btn-light btn-sm" rounded>
              <IconBase icon="fa-solid:eye" />
            </button>
          </div>
        </div>
      </div>
    </div>

    <button type="button" class="mt-3 btn btn-dark btn-rounded btn-block">
      Delete
    </button>

    <!-- Modals -->
    <teleport to="body">
      <v-dialog v-model="showColumnSettingsModal" width="500">
        <v-card>
          <v-card-text>
            <v-select :items="defaultColumnTypes" />
          </v-card-text>
        </v-card>
      </v-dialog>
    </teleport>
  </div>
</template>

<script setup lang="ts">
import { defaultColumnTypes } from 'src/data'
import { storeToRefs } from 'pinia'
import { useDatasource } from 'src/stores/datasources'
import { useSlides } from 'src/stores/slides'
import { onBeforeMount, ref } from 'vue'
import { ColumnTypes } from '@/types'
// import { toRef } from '@vueuse/core'

// import SheetSelection from '../SheetSelection.vue'

const slidesStore = useSlides()
const { currentSlide, blockRequestData } = storeToRefs(slidesStore)

const datasourceStore = useDatasource()
const { connections, currentConnection } = storeToRefs(datasourceStore)

const showColumnSettingsModal = ref<boolean>(false)

const sheetColumnsRequestData = ref()
const columnRequestData = ref()
const currentUpdatedColumn = ref<ColumnTypes>()

/**
 * Sets the selected column for update
 *
 * @param column The data of the column to be updated
 */
function handleChangeColumnSetting(column: ColumnTypes) {
  currentUpdatedColumn.value = columnRequestData.value[column.name]
  showColumnSettingsModal.value = true
}

/**
 * Retrieve the data for the
 * current slide
 */
// async function getSlideData() {
//   try {
//     if (this.currentSlide.slide_data_source) {
//       const response = await this.$http.get(`sheets/${this.currentSlide.slide_data_source}`)
//       this.slidesStore.currentSlideData = response.data.results
//       this.$session.create(this.currentSlide.slide_data_source, response.data.results)
//     }
//   } catch (e) {
//     console.log(e)
//   }
// }

/**
 * Change the source data for the
 * given slide
 */
// async function handleChangePageSource(sheetId) {
//   try {
//     const path = `slides/${this.currentSlide.slide_id}/update`
//     this.slideRequestData.slide_data_source = sheetId
//     const response = await this.$http.post(path, this.slideRequestData)

//     this.currentSlide.slide_data_source = response.data.slide_data_source
//     this.connectionsStore.setCurrentConnection(response.data.slide_data_source)
//     this.$session.create('slides', this.slidesStore.slides)

//     await this.getSlideData()
//   } catch (e) {
//     console.log(e)
//   }
// }

onBeforeMount(() => {
  console.log('DefaultSlideSidebar mounted (2)')
  // TODO: This sometimes has "undefined"
  console.log('current slide', this.currentSlide)

  // TODO: We are not able to load pre-exising connections
  // from the cache - maybe pass the connections via props ?
  // Create the field settings templates that we will
  // using to update the field settings
  // this.connections.columns.forEach((column) => {
  //   this.sheetColumnsRequestData[column] = {
  //     name: column,
  //     column_type: 'Text',
  //     conditions: []
  //   }
  // })
})

</script>
