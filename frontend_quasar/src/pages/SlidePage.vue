<template>
  <q-page padding>
    <div class="row">
      <div class="col-3 q-pr-sm">
        <q-card>
          <q-card-section>
            <div class="row">
              <div class="col-12">
                <q-input v-model="requestData.name" :rules="[maxLength]" class="q-mb-md" label="Name" outlined></q-input>
                <!-- @filter="filterFn" -->
                <q-select v-model="requestData.slide_data_source" label="Dataset" :options="sourcesIds" option-label="name" option-value="source_id" input-debounce="0" behavior="menu" use-input outlined></q-select>
              </div>
            </div>

            <div class="row">
              <div class="col-12 q-mt-lg">
                <p class="q-font-weight-bold">Columns</p>
                <q-list bordered separator>
                  <q-item v-for="column in dataSourcesSlide.currentSlideDataSource.columns" :key="column">
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

      <div class="col-9">
        <q-card class="q-mb-sm">
          <q-card-section>Left</q-card-section>
        </q-card>

        <!-- Blocks -->
        <component v-for="block in currentSlide.blocks" :is="block.component" :key="block.block_id" :block="block" />
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent } from 'vue'
import { useRules } from '../composables/rules'
import { ref } from 'vue'
import { storeToRefs, mapState } from 'pinia'
import { useSlides } from '../stores/slides'
import { useDataSources } from 'src/stores/connections'
import { useBlocksComposable } from '../composables/blocks'

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
    useBlocksComposable()
    const slidesStore = useSlides()
    const { currentSlide } = storeToRefs(slidesStore)
    const dataSourcesSlide = useDataSources()
    const { currentSlideDataSource } = storeToRefs(dataSourcesSlide)
    const requestData = ref({
      name: null,
      slide_data_source: null
    })
    const { maxLength } = useRules()
    return {
      dataSourcesSlide,
      currentSlideDataSource,
      slidesStore,
      currentSlide,
      requestData,
      maxLength
    }
  },
  computed: {
    ...mapState(useDataSources, ['sourcesIds'])
  },
  created () {
    this.slidesStore.setCurrentSlide(this.$route.params.id)
    this.dataSourcesSlide.setCurrentDataSource(this.currentSlide.slide_data_source)
  },
  beforeMount () {
    this.requestData.name = this.currentSlide.name
    this.requestData.slide_data_source = this.currentSlide.slide_data_source
  },
  methods: {
    filterFn (val, update) {
      if (val === '') {
        update(() => {
          options.value = stringOptions
        })
        return
      }

      update(() => {
        const needle = val.toLowerCase()
        options.value = stringOptions.filter(v => v.toLowerCase().indexOf(needle) > -1)
      })
    }
  }
})
</script>
