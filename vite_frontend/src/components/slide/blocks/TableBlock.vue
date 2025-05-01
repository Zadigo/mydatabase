<template>
  <q-card :id="`table-block-${blockDetails.block_id}`" :class="{ 'border border-info': isSelected }" class="shadow-sm" @click="handleBlockSelection">
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
            <th v-for="column in blockDetails.visible_columns" :key="column" class="text-left">
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
            <v-switch v-for="column in currentConnection.columns" :key="column" :label="column" inset hide-details />
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

            <!-- <v-switch v-for="column in blockDetails.record_creation_columns" :key="column" :label="column" inset hide-details /> -->
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
            <v-switch v-model="currentUpdatedColumn.allow_column_creation" label="Allow column creation" inset hide-details />
            <v-switch v-model="currentUpdatedColumn.allow_column_update" label="Allow column update" inset hide-details />
            <v-switch v-model="currentUpdatedColumn.allow_column_search" label="Allow column search" inset hide-details />
            <v-switch v-model="currentUpdatedColumn.column_visibility" label="Visibility" inset hide-details />
          </v-card-text>

          <v-card-actions>
            <v-btn @click="showColumnActionsModal = false">Cancel</v-btn>
            <v-btn variant="tonal" @click="handleUpdateColumn">Validate</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </teleport>
  </q-card>
</template>

<script setup lang="ts">
import { onBeforeMount, PropType, ref } from 'vue'
import { storeToRefs } from 'pinia'
import { getCurrentInstance } from 'vue'
import { useSlides } from 'src/store/slides'
import { useConnections } from 'src/stores/connections'
import { useBlocksComposable } from 'src/composables/blocks'
import { useUtilities } from 'src/composables/utils'

import NoSheetAlert from '../NoSheetAlert.vue'
import type { BlockItem } from 'src/types'
import { DefaultColumnTypes, DefaultSortingChoices } from 'src/data'
import { api } from 'src/boot/axios'

interface ColumRequestData {
  name: string
  column_type: DefaultColumnTypes,
  column_sort: DefaultSortingChoices
  column_visibility: boolean
  allow_column_creation: boolean
  allow_column_update: boolean
  allow_column_search: boolean
}

const props = defineProps({
  blockDetails: {
    type: Object as PropType<BlockItem>,
    required: true
  },
  isSelected: {
    type: Boolean,
    required: true
  }
})

const emit = defineEmits({
  'block-selected'(_data: BlockItem) {
    return true
  }
})

const app = getCurrentInstance()
const { listManager } = useUtilities()
const { columnTypeChoices, columnSortingChoices } = useBlocksComposable()
const slidesStore = useSlides()
const { currentSlide, blockRequestData, currentBlock } = storeToRefs(slidesStore)
const connectionsStore = useConnections()
const { currentConnection } = storeToRefs(connectionsStore)

const columnsRequestData = ref<Record<string, ColumRequestData>>({})

// const blockRequestData = ref({})
const showCreateRecordModal = ref<boolean>(false)
const showSearchRecordsModal = ref<boolean>(false)
const showColumnActionsModal = ref<boolean>(false)
const currentUpdatedColumn = ref<ColumRequestData | null>(null)

/**
 * Updates the current column conffiguration 
 * for the current block
 */
async function handleUpdateColumn () {
  try {
    if (currentSlide.value) {
      const path = `/api/v1/slides/${currentSlide.value.slide_id}/blocks/${currentBlock.block_id}/column/update`
      const response = await api.post(path, columnsRequestData.value[currentUpdatedColumn.value.name])
      
      currentBlock.visible_columns = response.data.visible_columns
      currentBlock.search_columns = response.data.search_columns
      currentBlock.record_update_columns = response.data.record_update_columns
      currentBlock.record_creation_columns = response.data.record_creation_columns
      showColumnActionsModal.value = false
      response.data
    }
  } catch (e) {
    console.log(e)
  }
}
/**
 * Shows the modal to set specific actions 
 * on a give column (search, visibility...)
 * 
 * @param columnName 
 */
function handleShowColumnActionModal(columnName: string) {
  columnsRequestData.value[columnName] = {
    name: columnName,
    column_type: 'Text',
    column_sort: 'No sort',
    column_visibility: props.blockDetails.visible_columns.includes(columnName),
    allow_column_creation: props.blockDetails.record_creation_columns.includes(columnName),
    allow_column_update: props.blockDetails.record_update_columns.includes(columnName),
    allow_column_search: props.blockDetails.search_columns.includes(columnName)
  }

  currentUpdatedColumn.value = columnsRequestData.value[columnName] || null
  showColumnActionsModal.value = true
}

/**
 * Highlights the block when the user 
 * has clicked on the card
 */
function handleBlockSelection () {
  slidesStore.setCurrentBlockRequestData()
  emit('block-selected', props.blockDetails)
}

onBeforeMount(() => {
  connectionsStore.loadFromCache()
  connectionsStore.setCurrentConnection(props.blockDetails.block_data_source || this.currentSlide.slide_data_source)
})
</script>
