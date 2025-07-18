<template>
  <base-card :id="`table-block-${blockDetails.block_id}`" :class="{ 'border border-info': isSelected }" class="shadow-sm" @click="handleBlockSelection">
    <template #header>
      <div class="d-flex justify-content-between align-items-center">
        <v-btn v-if="blockDetails.allow_record_search" elevation="0" variant="tonal" color="primary" rounded @click="showSearchRecordsModal = true">
          <font-awesome-icon :icon="['fas', 'search']" class="me-2" />
          Columns for search
        </v-btn>

        <div class="right-actions">
          <v-btn id="cta-user-filters" class="me-2" elevation="0" variant="tonal" color="primary" rounded @click.prevent>
            <font-awesome-icon :icon="['fas', 'filter']" class="me-2" />
            User filters
          </v-btn>
  
          <v-btn v-if="blockDetails.allow_record_creation" id="cta-create-record" elevation="0" variant="tonal" color="primary" rounded @click="showCreateRecordModal = true">
            <font-awesome-icon :icon="['fas', 'plus']" class="me-2" />
            Columns for creation
          </v-btn>
        </div>
      </div>
    </template>

    <template v-if="slidesStore.blockHasData || slidesStore.slideHasData" #body>
      <v-table fixed-header>
        <thead>
          <tr>
            <th v-for="column in currentConnection.columns" :key="column" class="text-left">
              <v-btn variant="tonal" rounded @click="handleShowColumnActionModal(column)">{{ column }}</v-btn>
            </th>
          </tr>
        </thead>

        <tbody>
          <template v-for="item in slidesStore.dataToUse" :key="item.index">
            <tr>
              <td v-for="column in blockDetails.visible_columns" :key="column">
                {{ item[column] }}
              </td>
            </tr>
          </template>
        </tbody>
      </v-table>
    </template>

    <template v-else #body>
      <no-sheet-alert />
    </template>

    <!-- Modals -->
    <teleport to="body">
      <v-dialog id="search-records-modal" v-model="showSearchRecordsModal" width="400">
        <v-card title="Select columns">
          <v-card-text>
            <p>Allow search on the specified columns</p>
            <v-switch v-for="column in currentConnection.columns" :key="column" :label="column" inset hide-details></v-switch>
          </v-card-text>

          <v-card-actions>
            <v-btn @click="showSearchRecordsModal = false">Cancel</v-btn>
            <v-btn>Validate</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </teleport>

    <teleport to="body">
      <v-dialog v-model="showCreateRecordModal" width="400">
        <v-card title="Select columns">
          <v-card-text>
            <p>Allow the creation for a new record for the specified columns</p>

            <div class="row">
              <!-- <div v-for="column in blockDetails.record_creation_columns" :key="column" class="col-12">
                <div class="d-flex justify-content-between align-items-center">
                  <span>{{ column }}</span>
                  <v-btn-toggle color="warning" multiple>
                    <v-btn value="creation">Create</v-btn>
                    <v-btn value="update">Update</v-btn>
                  </v-btn-toggle>
                </div>
              </div> -->
            </div>

            <!-- <v-switch v-for="column in blockDetails.record_creation_columns" :key="column" :label="column" inset hide-details></v-switch> -->
          </v-card-text>

          <v-card-actions>
            <v-btn>Cancel</v-btn>
            <v-btn>Validate</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </teleport>

    <teleport to="body">
      <v-dialog id="column-update-modal" v-model="showColumnActionsModal" width="500">
        <v-card>
          <v-card-text>
            <v-text-field v-model="currentUpdatedColumn.name" label="Column name" variant="outlined"></v-text-field>
            <v-select v-model="currentUpdatedColumn.column_type" :items="columnTypeChoices" label="Column type" variant="outlined"></v-select>
            <v-select v-model="currentUpdatedColumn.column_sort" :items="columnSortingChoices" label="Sort" variant="outlined" clearable hide-details></v-select>
            <v-switch v-model="currentUpdatedColumn.allow_column_creation" label="Allow column creation" inset hide-details></v-switch>
            <v-switch v-model="currentUpdatedColumn.allow_column_update" label="Allow column update" inset hide-details></v-switch>
            <v-switch v-model="currentUpdatedColumn.allow_column_search" label="Allow column search" inset hide-details></v-switch>
            <v-switch v-model="currentUpdatedColumn.column_visibility" label="Visibility" inset hide-details></v-switch>
          </v-card-text>

          <v-card-actions>
            <v-btn @click="showColumnActionsModal = false">Cancel</v-btn>
            <v-btn variant="tonal" @click="handleUpdateColumn">Validate</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </teleport>
  </base-card>
</template>

<script>
// import _ from 'lodash'
import { ref } from 'vue'
import { storeToRefs } from 'pinia'
import { getCurrentInstance } from 'vue'
import { useSlides } from '@/store/slides'
import { useConnections } from '@/store/connections'
import { useBlocksComposable } from '@/composables/blocks'
import { useUtilities } from '@/composables/utils'

import BaseCard from '../../layouts/bootstrap/cards/BaseCard.vue'
import NoSheetAlert from '../NoSheetAlert.vue'

export default {
  name: 'TableBlock',
  components: {
    BaseCard,
    NoSheetAlert
  },
  props: {
    blockDetails: {
      type: Object,
      required: true
    },
    isSelected: {
      type: Boolean,
      required: true
    }
  },
  emits: {
    'block-selected' () {
      return true
    }
  },
  setup () {
    const app = getCurrentInstance()
    const { listManager } = useUtilities()
    const { columnTypeChoices, columnSortingChoices } = useBlocksComposable(app)
    const slidesStore = useSlides()
    const { currentSlide, blockRequestData } = storeToRefs(slidesStore)
    const connectionsStore = useConnections()
    const { currentConnection } = storeToRefs(connectionsStore)
    const columnsRequestData = ref({})
    // const blockRequestData = ref({})
    // const isSelected = ref(false)
    const showCreateRecordModal = ref(false)
    const showSearchRecordsModal = ref(false)
    const showColumnActionsModal = ref(false)
    const currentUpdatedColumn = ref({})

    return {
      // isSelected,
      currentSlide,
      listManager,
      currentConnection,
      columnTypeChoices,
      columnSortingChoices,
      columnsRequestData,
      blockRequestData,
      currentUpdatedColumn,
      showCreateRecordModal,
      showSearchRecordsModal,
      showColumnActionsModal,
      slidesStore,
      connectionsStore
    }
  },
  beforeMount () {
    this.connectionsStore.loadFromCache()
    this.connectionsStore.setCurrentConnection(this.blockDetails.block_data_source || this.currentSlide.slide_data_source)
    
    // For each column create a template that will be used
    // to track configuration updates
    // _.forEach(this.connectionsStore.currentConnection.columns, (column) => {
    //   this.columnsRequestData[column] = {
    //     name: column,
    //     column_type: 'Text',
    //     column_sort: 'No sort',
    //     column_visibility: this.blockDetails.visible_columns.includes(column),
    //     allow_column_creation: this.blockDetails.record_creation_columns.includes(column),
    //     allow_column_update: this.blockDetails.record_update_columns.includes(column),
    //     allow_column_search: this.blockDetails.search_columns.includes(column)
    //   }
    // })
  },
  methods: {
    handleShowColumnActionModal (columnName) {
      // Shows the modal to set specific actions
      // on a give column (search, visibility...)
      this.columnsRequestData[columnName] = {
        name: columnName,
        column_type: 'Text',
        column_sort: 'No sort',
        column_visibility: this.blockDetails.visible_columns.includes(columnName),
        allow_column_creation: this.blockDetails.record_creation_columns.includes(columnName),
        allow_column_update: this.blockDetails.record_update_columns.includes(columnName),
        allow_column_search: this.blockDetails.search_columns.includes(columnName)
      }
      this.currentUpdatedColumn = this.columnsRequestData[columnName] || {}
      this.showColumnActionsModal = true
    },
    handleBlockSelection () {
      // Highlights the block when the user
      // has clicked on the card
      this.slidesStore.setCurrentBlockRequestData()
      this.$emit('block-selected', this.blockDetails)
    }
  }
}
</script>
