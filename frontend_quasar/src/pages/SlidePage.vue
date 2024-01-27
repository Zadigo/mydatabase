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
                <!-- @filter="filterFn" -->
                <q-select v-model="requestData.slide_data_source" label="Data source" :options="sourcesIds" option-label="name" option-value="source_id" input-debounce="0" behavior="menu" emit-value use-input outlined></q-select>
              </div>
            </div>

            <div class="row">
              <div class="col-12 q-mt-lg">
                <p class="q-font-weight-bold">Columns</p>
                <q-list bordered separator>
                  <q-item v-for="column in dataSourcesStore.currentSlideDataSource.columns" :key="column">
                    <q-item-section>
                      <q-item-label>{{ column }}</q-item-label>
                    </q-item-section>

                    <q-item-section side>
                      <div class="row">
                        <q-btn size="sm" rounded flat>
                          <q-icon name="chat_bubble" color="grey" />
                        </q-btn>

                        <q-btn size="sm" rounded flat>
                          <q-icon name="chat_bubble" color="grey" />
                        </q-btn>
                      </div>
                    </q-item-section>
                  </q-item>
                </q-list>
              </div>
            </div>

            <div class="row q-mt-xl">
              <div class="col-12">
                <q-btn color="primary" block flat rounded>Delete</q-btn>
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>

      <!-- Header -->
      <div class="col-9">
        <q-card class="q-mb-sm">
          <q-card-section>
            <q-btn v-for="action in blockActions" :key="action.component" color="primary" flat @click="handleCreateBlock">
              {{ action.icon }}
            </q-btn>

            <q-btn v-if="requiresSaving" color="primary" @click="requestUpdateSlide">Save</q-btn>
          </q-card-section>
        </q-card>

        <!-- Blocks -->
        <component :is="block.component" v-for="block in currentSlide.blocks" :key="block.block_id" :block="block" />
      </div>
    </div>
  </q-page>
</template>

<script>
import _ from 'lodash'
import { defineComponent } from 'vue'
import { useRules } from '../composables/rules'
import { ref, getCurrentInstance } from 'vue'
import { storeToRefs, mapState } from 'pinia'
import { useSlides } from '../stores/slides'
import { useDataUpdating } from '../composables/updating'
import { useDataSources } from 'src/stores/connections'
import { useQuasar } from 'quasar'
// import { useBlocksComposable } from '../composables/blocks'

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
    const notifications = useQuasar()

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
        icon: 'table'
      }
    ]
    return {
      notifications,
      blockActions,
      requiresSaving,
      canBeSaved,
      isSaved,
      filteredSourceIds,
      dataSourcesStore,
      currentSlideDataSource,
      slidesStore,
      currentSlide,
      requestData,
      blockRequestData,
      maxLength
    }
  },
  computed: {
    ...mapState(useDataSources, ['sourcesIds'])
  },
  created () {
    this.slidesStore.setCurrentSlide(this.$route.params.id)
    this.dataSourcesStore.setCurrentDataSource(this.currentSlide.slide_data_source)
  },
  beforeMount () {
    this.requestData.name = this.currentSlide.name
    this.requestData.slide_data_source = this.currentSlide.slide_data_source
  },
  methods: {
    async requestUpdateSlide () {
      // Update pieces of information for the current slide
      // Once the inforamation is updated, another api call
      // is made to get information on the new data source
      try {
        const response = await this.$api.post(`slides/${this.currentSlide.slide_id}/update`, this.requestData)
        
        this.currentSlide = response.data
        this.isSaved = true

        const response_two = await this.$api.get(`sheets/${this.currentSlide.slide_data_source}`)
        this.currentSlideDataSource = response_two.data
        this.$session.dictSet('sources', this.currentSlide.sheet_id, dataResults)

        this.notifications.notify({
          message: 'Slide updated',
          color: 'green'
        })
      } catch (error) {
        this.notifications.notify({
          message: 'Could not update slide',
          color: 'danger'
        })
      }
    },
    async handleCreateBlock () {
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
    selectFilter (val, update) {
      if (val === "") {
        update(() => {
          this.filteredSourceIds = this.sourcesIds
        })
        return
      }

      update(() => {
        const name = val.toLowerCase()
        this.filteredSourceIds = _.filter(this.sourceIds, (source) => {
          return source.name.toLowerCase().indexOf(name) > -1
        })
        // options.value = stringOptions.filter(v => v.toLowerCase().indexOf(needle) > -1)
      })
    }
  }
})
</script>
