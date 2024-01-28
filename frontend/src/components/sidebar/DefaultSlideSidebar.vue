<template>
  <div id="inner-sidebar" class="my-1">
    <v-text-field v-model="slideRequestData.name" variant="outlined" elevation="0" placeholder="Slide name" />    
    <v-select id="sheet-selection" v-model="slideRequestData.slide_data_source" :items="connections" item-title="name" item-value="sheet_id" placeholder="Select sheet" variant="outlined" hide-details @update:model-value="handleChangePageSource"></v-select>

    <!-- Columns -->
    <div class="mt-5">
      <h2 class="h6">Columns</h2>
      <div class="list-group">
        <div v-for="column in currentConnection.columns" :key="column" class="list-group-item list-group-item-action p-3 d-block">
          <span class="fw-bold">{{ column }}</span>
          <div class="mt-2">
            <v-btn class="me-1" variant="tonal" density="compact" @click="handleChangeColumnSetting(column)" rounded>
              <font-awesome-icon :icon="['fa', 'cog']" />
            </v-btn>
            <v-btn variant="tonal" density="compact" rounded>
              <font-awesome-icon :icon="['fa', 'eye']" />
            </v-btn>
          </div>
        </div>
      </div>
    </div>

    <v-btn class="mt-3" variant="tonal" color="danger" rounded block>
      Delete
    </v-btn>

    <!-- Modals -->
    <teleport to="body">
      <v-dialog v-model="showColumnSettingsModal" width="500">
        <v-card>
          <v-card-text>
            <v-select :items="columnTypes" variant="solo" />
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
    const sheetColumnsRequestData = ref({})
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
      sheetColumnsRequestData,
      slideRequestData,
      currentSlide,
      connectionsStore,
      slidesStore
    }
  },
  beforeMount () {
    console.log('DefaultSlideSidebar mounted (2)')
    // TODO: This sometimes has "undefined"
    console.log('current slide', this.currentSlide)
    Object.keys(this.slideRequestData).forEach((key) => {
      this.slideRequestData[key] = this.currentSlide[key]
    })

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
  },
  methods: {
    handleChangeColumnSetting (columnName) {
      // Set the current column being updated
      this.currentUpdatedColumn = this.columnRequestData[columnName]
      this.showColumnSettingsModal = true
    },
    async getSlideData () {
      // Retrieve the data for the 
      // current slide
      try {
        if (this.currentSlide.slide_data_source) {
          const response = await this.$http.get(`sheets/${this.currentSlide.slide_data_source}`)
          this.slidesStore.currentSlideData = response.data.results
          this.$session.create(this.currentSlide.slide_data_source, response.data.results)
        }
      } catch (e) {
        console.log(e)
      }
    },
    async handleChangePageSource (sheetId) {
      // Change the source data for the 
      // given slide
      try {
        const path = `slides/${this.currentSlide.slide_id}/update`
        this.slideRequestData.slide_data_source = sheetId
        const response = await this.$http.post(path, this.slideRequestData)

        this.currentSlide.slide_data_source = response.data.slide_data_source
        this.connectionsStore.setCurrentConnection(response.data.slide_data_source)
        this.$session.create('slides', this.slidesStore.slides)

        await this.getSlideData()
      } catch (e) {
        console.log(e)
      }
    }
  }
}
</script>

<style scoped>
/* #inner-sidebar {
  overflow-y: scroll;
  height: 550px;
} */
</style>
