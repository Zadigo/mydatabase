<template>
  <q-page padding>
    <div class="row">
      <!-- Sidebar -->
      <div class="col-3 q-pr-sm">
        <q-card>
          <q-card-section>
            <div class="row">
              <div class="col-12">
                <q-input v-model="requestData.name" :rules="[maxLength]" class="q-mb-md" label="Name" outlined></q-input>
                <q-select v-model="requestData.slide_data_source" :options="dataSourcesStore.dataSources" option-label="name" option-value="data_source_id" emit-value outlined></q-select>
                <!-- TODO: This emits the whole object on requestData -->
                <!-- <q-select v-model="requestData.slide_data_source" label="Data source" :options="dataSourcesStore.dataSources" option-label="name" option-value="data_source_id" emit-value use-input outlined></q-select> -->
              </div>
            </div>

            <!-- Columns -->
            <div v-if="currentSlideDataSource" class="row">
              <div class="col-12 q-mt-lg">
                <p class="q-font-weight-bold">Columns</p>
                <q-list bordered separator>
                  <q-item v-for="column in dataSourcesStore.currentSlideDataSource.columns" :key="column">
                    <q-item-section>
                      <q-item-label><q-icon name="fas fa-font"></q-icon></q-item-label>
                      <q-item-label>{{ conditionalTruncate(column.name, 20, 15) }}</q-item-label>
                    </q-item-section>

                    <q-item-section side>
                      <div class="row">
                        <!-- <q-btn size="sm" rounded flat>
                          <q-icon name="chat_bubble" color="grey" />
                        </q-btn> -->

                        <q-btn size="sm" round flat @click="handleShowColumnSettings(column)">
                          <q-icon name="fas fa-cog" size="1.3em" />
                        </q-btn>
                      </div>
                    </q-item-section>
                  </q-item>
                </q-list>
              </div>
            </div>

            <div class="row q-mt-xl">
              <div class="col-12">
                <q-btn class="text-black" color="red-1" style="width: 100%;" block unelevated rounded>
                  {{ $t('Delete') }}
                </q-btn>
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>

      <div class="col-9">
        <!-- Header -->
        <q-card tag="header" class="q-mb-sm">
          <q-card-section>
            <div class="flex justify-between align-center">
              <div class="actions left">
                <q-btn v-for="action in blockActions" :key="action.component" color="grey-3" class="text-black q-mr-sm" round unelevated @click="handleCreateBlock">
                  <q-icon :name="action.icon" size="1em"></q-icon>
                </q-btn>
              </div>
  
              <div class="actions-right">
                <q-btn v-if="requiresSaving" class="q-mr-sm" color="primary" rounded unelevated @click="requestUpdateSlide">
                  <q-icon name="fas fa-save" class="q-mr-sm" size="1em"></q-icon>
                  {{ $t('Save') }}
                </q-btn>
                
                <q-btn :to="{ name: 'slide_visualization', params: { id: currentSlide.slide_id }, query: { preview: true }}" color="secondary" rounded unelevated>
                  <q-icon name="fas fa-eye" class="q-mr-sm" size="1em"></q-icon>
                  {{ $t('Preview') }}
                </q-btn>
              </div>
            </div>
          </q-card-section>
        </q-card>

        <!-- Blocks -->
        <component :is="block.component" v-for="block in currentSlide.blocks" :key="block.block_id" :block="block" />
        <q-card>
          <q-card-section>
            <h3>No data source</h3>
          </q-card-section>
        </q-card>
      </div>
    </div>

    <!-- Modals -->
    <q-dialog v-model="showColumnSettingsModal" persistent>
      <q-card style="width: 400px;">
        <q-card-section>
          <q-input v-model="currentUpdatedColumn.name" outlined></q-input>
          <q-toggle v-model="currentUpdatedColumn.visibility" label="Column is visible"></q-toggle>
          <q-select v-model="currentUpdatedColumn.column_type" :options="columnTypes" outlined></q-select>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat @click="handleCancelColumnSettings">Cancel</q-btn>
          <q-btn color="dark" flat @click="handleSaveColumnSettings">Save</q-btn>
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script>
import _ from 'lodash'
import { useUtilities } from '../../composables/utils'
import { useQuasar } from 'quasar'
import { defineComponent } from 'vue'
import { ref, getCurrentInstance } from 'vue'
import { storeToRefs } from 'pinia'
import { useRules } from '../../composables/rules'
import { useSlides } from '../../stores/slides'
import { useDataUpdating } from '../../composables/updating'
import { useDataSources } from 'src/stores/connections'
// import { useBlocksComposable } from '../composables/blocks'

import columnTypes from '../../data/column_types.json'

import GraphBlock from 'src/components/GraphBlock.vue'
import KanbanBlock from 'src/components/KanbanBlock.vue'
import TableBlock from 'src/components/TableBlock.vue'

export default defineComponent({
  name: 'SlidePage',
  components: {
    GraphBlock,
    KanbanBlock,
    TableBlock
  },
  setup () {
    const { conditionalTruncate } = useUtilities()
    const notifications = useQuasar()

    const showColumnSettingsModal = ref(false)
    const currentUpdatedColumn = ref({
      name: null,
      visibility: true,
      column_type: 'Text'
    })

    const app = getCurrentInstance()
    const { requiresSaving, canBeSaved, isSaved } = useDataUpdating(app, ['name', 'slide_data_source'])

    const slidesStore = useSlides()
    const { currentSlide } = storeToRefs(slidesStore)
    
    const dataSourcesStore = useDataSources()
    const { currentSlideDataSource } = storeToRefs(dataSourcesStore)
    
    const requestData = ref({
      name: null,
      slide_data_source: null
    })
    const blockRequestData = ref({
      name: null,
      active: true,
      component: 'table-block',
      record_creation_columns: [],
      record_update_columns: [],
      search_columns: [],
      user_filters: [],
      conditions: {
        columns_visibility: [],
        filters: []
      }
    })

    const { maxLength } = useRules()
    const filteredSourceIds = ref([])
    const blockActions = [
      {
        component: 'table-block',
        icon: 'fas fa-table'
      },
      {
        component: 'chart-block',
        icon: 'fas fa-chart-simple'
      }
    ]
    return {
      columnTypes,
      notifications,
      blockActions,
      requiresSaving,
      canBeSaved,
      isSaved,
      filteredSourceIds,
      dataSourcesStore,
      currentSlideDataSource,
      showColumnSettingsModal,
      currentUpdatedColumn,
      slidesStore,
      currentSlide,
      requestData,
      blockRequestData,
      maxLength,
      conditionalTruncate
    }
  },
  computed: {
    // ...mapState(useDataSources, ['sourcesIds'])
  },
  created () {
    this.slidesStore.setCurrentSlide(this.$route.params.id)
    // TODO: Check if needed
    this.dataSourcesStore.currentSlideDataSource = this.currentSlide.slide_data_source
  },
  beforeMount () {
    this.requestData.name = this.currentSlide.name
    this.requestData.slide_data_source = this.dataSourcesStore.currentSlideDataSource?.data_source_id
  },
  methods: {
    async requestUpdateColumns () {

    },
    async requestUpdateSlide () {
      // Update pieces of information for the current slide
      // Once the inforamation is updated, another api call
      // is made to get information on the new data source
      try {
        const response = await this.$api.post(`slides/${this.currentSlide.slide_id}/update`, this.requestData)
        
        this.currentSlide = response.data
        this.isSaved = true

        const response_two = await this.$api.get(`datasources/${this.currentSlide.slide_data_source.data_source_id}`)
        this.currentSlideDataSource = response_two.data
        this.$session.dictSet('sources', this.currentSlide.sheet_id, this.currentSlideDataSource)

        this.notifications.notify({
          message: 'Slide updated',
          color: 'green-4',
          position: 'top',
          timeout: 1000,
          closeBtn: true
        })
      } catch (error) {
        console.log(error)
        this.notifications.notify({
          message: 'Could not update slide',
          position: 'top',
          color: 'red-4',
          timeout: 1000,
          closeBtn: true
        })
      }
    },
    async handleCreateBlock () {
      // Creates a new block for the current
      // slide in the backend
      try {
        const response = await this.$api.post(`slides/${this.currentSlide.slide_id}/blocks/create`, this.blockRequestData)
        this.currentSlide.blocks.push(response.data)
        this.notifications.notify({
          message: 'Block created',
          color: 'green'
        })
      } catch (error) {
        this.notifications.notify({
          message: 'Could not create block',
          color: 'danger'
        })
      }
    },
    handleCancelColumnSettings () {
      this.currentUpdatedColumn.name = null
      this.currentUpdatedColumn.visibility = true
      this.currentUpdatedColumn.column_type = 'Text'
      this.showColumnSettingsModal = false
    },
    handleSaveColumnSettings () {
      this.handleCancelColumnSettings()
    },
    handleShowColumnSettings (column) {
      // Handles the display of the 
      // column settings modal
      this.currentUpdatedColumn.name = column.name
      this.showColumnSettingsModal = true
    },
    // selectFilter (val, update) {
    //   if (val === "") {
    //     update(() => {
    //       this.filteredSourceIds = this.sourcesIds
    //     })
    //     return
    //   }

    //   update(() => {
    //     const name = val.toLowerCase()
    //     this.filteredSourceIds = _.filter(this.sourceIds, (source) => {
    //       return source.name.toLowerCase().indexOf(name) > -1
    //     })
    //     // options.value = stringOptions.filter(v => v.toLowerCase().indexOf(needle) > -1)
    //   })
    // }
  }
})
</script>
