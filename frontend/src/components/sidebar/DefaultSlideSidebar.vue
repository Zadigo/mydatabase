<template>
  <div id="inner-sidebar" class="p-4 my-4">
    <v-text-field v-model="slideRequestData.name" variant="outlined" elevation="0" placeholder="Page name" />    
    <v-select id="sheet-selection" v-model="slideRequestData.slide_data_source" :items="connections" item-title="name" item-value="sheet_id" placeholder="Select sheet" variant="outlined" clearable hide-details @update:model-value="handleChangePageSource"></v-select>

    <!-- Columns -->
    <div class="mt-5">
      <h2 class="h6">Columns</h2>
      <div class="list-group">
        <div v-for="column in currentConnection.columns" :key="column" class="list-group-item list-group-item-action p-3 d-block">
          <span class="fw-bold">{{ column }}</span>
          <div class="mt-2">
            <v-btn class="me-1" variant="tonal" density="compact" @click="handleChangeColumnSetting(column)"></v-btn>
            <v-btn variant="tonal" density="compact"></v-btn>
          </div>
        </div>
      </div>
    </div>

    <v-btn class="mt-3" variant="tonal" rounded block>Delete</v-btn>

    <!-- Modals -->
    <teleport to="body">
      <v-dialog v-model="showColumnSettingsModal" width="500">
        <v-card>
          <v-card-text>
            <v-select v-model="currentUpdatedColumn.column_type" :items="columnTypes" variant="solo" />
          </v-card-text>
        </v-card>
      </v-dialog>
    </teleport>
  </div>
</template>

<script>
import { useConnections } from '@/store/connections'
import { useSlides } from '@/store/slides'
import { storeToRefs } from 'pinia'
import { ref } from 'vue'

// import SheetSelection from '../SheetSelection.vue'

export default {
  name: 'DefaultPageSidebar',
  setup () {
    const slidesStore = useSlides()
    const { currentSlide } = storeToRefs(slidesStore)
    const connectionsStore = useConnections()
    const { connections, currentConnection } = storeToRefs(connectionsStore)
    const showColumnSettingsModal = ref(false)
    const slideRequestData = ref({
      name: null,
      slide_data_source: null
    })    
    const columnRequestData = ref({})
    const currentUpdatedColumn = ref({})
    const columnTypes = ref([
      'Text',
      'Date',
      'Link',
      'Number'
    ])
 
    return {
      connections,
      columnTypes,
      currentConnection,
      currentUpdatedColumn,
      showColumnSettingsModal,
      columnRequestData,
      slideRequestData,
      currentSlide,
      slidesStore
    }
  },
  mounted () {
    Object.keys(this.slideRequestData).forEach((key) => {
      this.slideRequestData[key] = this.currentSlide[key]
    })

    // // TODO: Generates an error when refreshing the page
    // this.slideRequestData.name = this.currentSlide.name
    // this.slideRequestData.page_url_source = this.currentSlide.slide_data_source

    // this.getData()
    // // Create the field settings templates that we will
    // // using to update the field settings
    // this.slidesStore.currentSlideData.columns.forEach((column) => {
    //   this.columnRequestData[column] = {
    //     name: column,
    //     column_type: 'Text',
    //     conditions: []
    //   }
    // })
  },
  methods: {
    handleChangeColumnSetting (columnName) {
      // Set the current column being updated
      this.currentUpdatedColumn = this.columnRequestData[columnName]
      this.showColumnSettingsModal = true
    },
    async getData () {
      // Retrieve the data for the current page
      try {
        if (this.currentPage.page_url_source) {
          const response = await this.$http.get(`sheets/${this.currentPage.page_url_source}`)
          this.slidesStore.currentSlideData = response.data
        }
      } catch (e) {
        console.log(e)
      }
    },
    async handleChangePageSource (sheetId) {
      // Change the source for the given page
      try {
        const path = `sheets/pages/${this.currentPage.page_id}/update`
        this.slideRequestData.page_data_source = sheetId
        const response = await this.$http.post(path, this.slideRequestData)
        this.slidesStore.currentPage = response.data
        await this.getData()
      } catch (e) {
        console.log(e)
      }
    }
  }
}
</script>

<style scoped>
#inner-sidebar {
  overflow-y: scroll;
  height: 550px;
}
</style>
