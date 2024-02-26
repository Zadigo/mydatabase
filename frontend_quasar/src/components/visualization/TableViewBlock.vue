<template>
  <q-card>
    <!-- Actions -->
    <q-card-section>
      <div class="row">
        <div class="col-6">
          <q-input type="search" style="width: 60%;" placeholder="Search..." outlined>
            <template v-slot:prepend>
              <q-icon name="fas fa-search" size=".8em" />
            </template>
          </q-input>
        </div>

        <div class="col-6 text-right">
          <q-btn v-if="block.allow_record_creation" class="q-mr-sm" color="primary" unelevated rounded>
            Create
          </q-btn>
          
          <q-btn class="q-mr-md" color="secondary" rounded @click="showBlockSettings = true">
            <q-icon name="fas fa-cog" size="1em"></q-icon>
          </q-btn>

          <q-btn class="q-mr-md" color="primary" rounded>
            <q-icon name="fas fa-filter" size="1em" class="q-mr-md"></q-icon>
            Filter

            <q-menu>
              <q-list>
                <q-item v-for="(column, x) in tableColumns" :key="x" v-close-popup clickable @click="handleAddFilter(column)">
                  <q-item-section>
                    {{ column.name }}
                  </q-item-section>

                </q-item>

                <q-separator />
                
                <q-item v-close-popup clickable>
                  <q-item-section>
                    <q-icon name="fas fa-plus"></q-icon>
                  </q-item-section>

                  <q-item-section>
                    Advanced filter
                  </q-item-section>
                </q-item>
              </q-list>
            </q-menu>
          </q-btn>

          <q-btn color="primary" rounded>
            <q-icon name="fas fa-refresh" size="1em" class="q-mr-md"></q-icon>
            Refresh
          </q-btn>
        </div>
      </div>

      <!-- Filters -->
      <div v-if="hasFilters" class="row q-mt-md">
        <div class="col-12">
          <q-btn v-for="(item, i) in blockFilters" :key="i" class="q-mr-sm" color="primary" outline rounded>
            {{ item.column }}: {{ item.value }} <q-icon name="fas fa-caret-down q-ml-sm" size="1em"></q-icon>

            <q-menu>
              <q-list>
                <q-item>
                  <q-item-section>
                    <q-btn size="sm" flat>
                      {{ item.operator }}

                      <q-menu>
                        <q-list>
                          <q-item v-for="operator in filteringOperators" :key="operator" clickable @click="() => { item.operator = operator }">
                            <q-item-section>
                              {{ operator }}
                            </q-item-section>
                          </q-item>
                        </q-list>
                      </q-menu>
                    </q-btn>
                  </q-item-section>

                  <q-item-section v-if="item.operator !== 'Empty' && item.operator !== 'Not empty'">
                    <q-input v-model="item.value" outlined clearable @keypress="requestDataFiltering"></q-input>
                  </q-item-section>
                </q-item>
              </q-list>
            </q-menu>
          </q-btn>
        </div>
      </div>
    </q-card-section>

    <!-- Table -->
    <q-card-section>
      <q-table v-model:pagination="pagination" :rows-per-page-options="[0]" :columns="tableColumns" :rows="actualBlockData.results" :elevation="0" virtual-scroll flat></q-table>
    </q-card-section>

    <!-- Modals -->
    <q-dialog v-model="showBlockSettings">
      <q-card style="width: 900px; max-width: 80vw;">
        <q-card-section>
          <q-splitter v-model="splitterModel" style="height: 400px">
            <template v-slot:before>
              <div class="q-pa-md">
                <q-tree v-model:selected="selected" :nodes="simple" node-key="label" selected-color="primary" default-expand-all />
              </div>
            </template>

            <template v-slot:after>
              <q-tab-panels v-model="selected" animated transition-prev="jump-up" transition-next="jump-up">
                <q-tab-panel name="Relax Hotel">
                  <div class="text-h4 q-mb-md">Welcome</div>
                  <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quis praesentium cumque magnam odio iure quidem, quod illum numquam possimus obcaecati commodi minima assumenda consectetur culpa fuga nulla ullam. In, libero.</p>
                  <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quis praesentium cumque magnam odio iure quidem, quod illum numquam possimus obcaecati commodi minima assumenda consectetur culpa fuga nulla ullam. In, libero.</p>
                </q-tab-panel>

                <q-tab-panel name="Food">
                  <div class="text-h4 q-mb-md">Column visibility</div>
                  <q-list bordered separator>
                    <q-item v-for="(column, i) in visibleTableColumns" :key="i">
                      <q-item-section>
                        {{ column.name }}
                      </q-item-section>

                      <q-item-section side>
                        <q-toggle v-model="column.visible"></q-toggle>
                      </q-item-section>
                    </q-item>
                  </q-list>
                </q-tab-panel>

                <q-tab-panel name="Room service">
                  <div class="text-h4 q-mb-md">Room service</div>
                  <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quis praesentium cumque magnam odio iure quidem, quod illum numquam possimus obcaecati commodi minima assumenda consectetur culpa fuga nulla ullam. In, libero.</p>
                  <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quis praesentium cumque magnam odio iure quidem, quod illum numquam possimus obcaecati commodi minima assumenda consectetur culpa fuga nulla ullam. In, libero.</p>
                  <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quis praesentium cumque magnam odio iure quidem, quod illum numquam possimus obcaecati commodi minima assumenda consectetur culpa fuga nulla ullam. In, libero.</p>
                </q-tab-panel>

                <q-tab-panel name="Room view">
                  <div class="text-h4 q-mb-md">Room view</div>
                  <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quis praesentium cumque magnam odio iure quidem, quod illum numquam possimus obcaecati commodi minima assumenda consectetur culpa fuga nulla ullam. In, libero.</p>
                  <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quis praesentium cumque magnam odio iure quidem, quod illum numquam possimus obcaecati commodi minima assumenda consectetur culpa fuga nulla ullam. In, libero.</p>
                </q-tab-panel>
              </q-tab-panels>
            </template>
          </q-splitter>
        </q-card-section>
      </q-card>
    </q-dialog>
  </q-card>
</template>

<script>
import _ from 'lodash'
import { useQuasar } from 'quasar'
import { defineComponent, ref } from 'vue'

export default defineComponent({
  name: 'TableViewBlock',
  props: {
    block: {
      type: Object
    },
    slideDataResults: {
      type: Object
    }
  },
  setup () {
    const quasar = useQuasar()
    const pagination = ref({
      rowsPerPage: 10
    })
    const splitterModel = ref(30)

    const visibleTableColumns = ref([])
    const showBlockSettings = ref(false)
    const blockFilters = ref([])

    const filteringOperators = [
      'Is',
      'Is not',
      'Contains',
      'Does not contain',
      'Starts with',
      'Ends with',
      'Empty',
      'Not empty'
    ]

    const selected = ref('Food')
    const  simple = [
        {
          label: 'Relax Hotel',
          children: [
            {
              label: 'Food',
              icon: 'restaurant_menu'
            },
            {
              label: 'Room service',
              icon: 'room_service'
            },
            {
              label: 'Room view',
              icon: 'photo'
            }
          ]
        }
      ]

      const actualBlockData = ref({})
    return {
      quasar,
      actualBlockData,
      splitterModel,
      filteringOperators,
      visibleTableColumns,
      selected,
      simple,
      showBlockSettings,
      pagination,
      blockFilters
      // tableColumns
    }
  },
  computed: {
    hasFilters () {
      // Checks if the block has filters to
      // be used to display the data
      return this.blockFilters.length > 0
    },
    tableColumns () {
      const a = []
      _.forEach(this.visibleTableColumns, (item) => {
      
        if (item.visible) {
          a.push({
            name: item.name,
            label: item.name,
            field: item.name,
            sortable: true
          })
        }
      })
      return a
    }
  },
  created () {
    
    setTimeout(() => {
      // Since we might have two different data
      // sources, copy the slide data source to
      // actualBlockData which we can then modify
      // freely
      Object.assign(this.actualBlockData, this.slideDataResults)

      this.visibleTableColumns = _.map(this.block.active_data_source.column_names, (column) => {
        return {
          name: column,
          visible: true
        }
      })
    }, 500)
  },
  beforeMount () {
    this.requestBlockDataSource()
  },
  methods: {
    async requestBlockDataSource () {
      // pass
    },
    requestDataFiltering: _.debounce(async function () {
      try {
        const slideId = this.$route.params.id
        const blockId = this.block.block_id
        const response = await this.$api.post(`/slides/${slideId}/blocks/${blockId}/filter`, {
          slide_id: slideId,
          block_id: blockId,
          data_source_id: this.slideDataResults.data_source_id,
          conditions: this.blockFilters,
          data: this.slideDataResults
        })
        this.actualBlockData.results = response.data.results
      } catch (e) {
        // this.quasar.$notify({
        //   message: 'Could not run filter'
        // })
        console.log(e)
      }
    }, 1000),
    handleAddFilter (column) {
      this.blockFilters.push({
        column: column.name,
        operator: 'Is',
        value: null,
        union: 'and'
      })
    }
  }
})
</script>
