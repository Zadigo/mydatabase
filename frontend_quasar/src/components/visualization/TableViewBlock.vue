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
          <q-btn class="q-mr-md" color="secondary" rounded @click="showBlockSettings = true">
            <q-icon name="fas fa-cog" size="1em"></q-icon>
          </q-btn>

          <q-btn class="q-mr-md" color="primary" rounded>
            <q-icon name="fas fa-filter" size="1em" class="q-mr-md"></q-icon>
            Filter

            <q-menu>
              <q-list>
                <q-item v-for="column in tableColumns" :key="column.name" v-close-popup clickable @click="handleAddFilter(column)">
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

      <div v-if="hasFilters" class="row q-mt-md">
        <div class="col-12">
          <q-btn v-for="(item, i) in blockFilters" :key="i" class="q-mr-sm" color="primary" outline rounded>
            {{ item.name }}: {{ item.value }} <q-icon name="fas fa-caret-down q-ml-sm" size="1em"></q-icon>

            <q-menu>
              <q-list>
                <q-item>
                  <q-item-section>
                    <q-btn size="sm" flat>
                      {{ item.condition }}

                      <q-menu>
                        <q-list>
                          <q-item v-for="condition in filteringConditions" :key="condition" v-close-popup clickable @click="() => { item.condition = condition }">
                            <q-item-section>
                              {{ condition }}
                            </q-item-section>
                          </q-item>
                        </q-list>
                      </q-menu>
                    </q-btn>
                  </q-item-section>

                  <q-item-section>
                    <q-input v-model="item.value" outlined clearable></q-input>
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
      <q-table v-model:pagination="pagination" :rows-per-page-options="[0]" :columns="tableColumns" :rows="slideDataResults.results" :elevation="0" virtual-scroll flat></q-table>
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
    const pagination = ref({
      rowsPerPage: 10
    })
    const splitterModel = ref(30)
    // const tableColumns = ref([])
    const visibleTableColumns = ref([])
    const showBlockSettings = ref(false)
    const blockFilters = ref([])

    const filteringConditions = [
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
    return {
      splitterModel,
      filteringConditions,
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
    _filteredResults () {
      if (this.hasFilters) {
        let filteredResults = []

        function isFilter (f, data) {
          return _.filter(data, (item) => {
            return item[f.name] === f.value
          })    
        }

        function containsFilter (f, data) {
          return _.filter(data, (item) => {
            return item[f.name].includes(f.value)
          })
        }

        _.forEach(this.blockFilters, (blockFilter) => {
          if (filteredResults.length > 0) {
            switch (blockFilter.condition) {
              case 'Is':
                filteredResults = isFilter(blockFilter, filteredResults)
                break

              case 'Contains':
                filteredResults = containsFilter(blockFilter, filteredResults)
                break
            
              default:
                break
            }
          } else {
            switch (blockFilter.condition) {
              case 'Is':
                filteredResults = isFilter(blockFilter, this.slideDataResults.results)
                break

              case 'Contains':
                filteredResults = containsFilter(blockFilter, filteredResults)
                break

              default:
                break
            }
          }
        })
        return filteredResults
      } else {
        return this.slideDataResults.results
      }
    },
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
            field: item.name
          })
        }
      })
      return a
    }
  },
  created () {
    setTimeout(() => {
      this.visibleTableColumns = _.map(this.slideDataResults.columns, (column) => {
        return {
          name: column,
          visible: true
        }
      })
    }, 500)
  },
  beforeMount () {
    if (!this.block.block_data_source) {
      this.requestBlockDataSource()
    }
  },
  methods: {
    async requestBlockDataSource () {
      // pass
    },
    handleAddFilter (column) {
      this.blockFilters.push({
        name: column.name,
        condition: 'Is',
        value: null
      })
    }
  }
})
</script>
