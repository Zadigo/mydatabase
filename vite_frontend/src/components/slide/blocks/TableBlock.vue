<template>
  <div :id="`table-block-${blockDetails.block_id}`" :class="{ 'border border-info': isSelected }" class="card shadow-sm" @click="handleBlockSelection">
    <div class="card-header">
      <div class="d-flex justify-content-between align-items-center">
        <button v-if="blockDetails.allow_record_search" elevation="0" class="btn btn-primary" @click="showSearchRecordsModal=true">
          <IconBase name="'fas-solid:search" class="me-2" />
          Columns for search
        </button>

        <div class="right-actions">
          <button id="cta-user-filters" class="me-2 btn btn-primary btn-sm" rounded @click.prevent>
            <IconBase name="'fas-solid:filter" class="me-2" />
            User filters
          </button>

          <button v-if="blockDetails.allow_record_creation" id="cta-create-record" class="btn btn-primary btn-sm" rounded @click="showCreateRecordModal=true">
            <IconBase name="'fas-solid:plus" class="me-2" />
            Columns for creation
          </button>
        </div>
      </div>
    </div>

    <div v-if="slidesStore.blockHasData || slidesStore.slideHasData" class="card-body">
      <v-table fixed-header>
        <thead>
          <tr>
            <th v-for="column in blockDetails.visible_columns" :key="column.name" class="text-left">
              <button variant="tonal" rounded @click="handleShowColumnActionModal(column)">
                {{ column.name }}
              </button>
            </th>
          </tr>
        </thead>

        <tbody>
          <template v-for="item in slidesStore.dataToUse" :key="item.index">
            <tr>
              <td v-for="column in blockDetails.visible_columns" :key="column.name">
                {{ item[column.name] }}
              </td>
            </tr>
          </template>
        </tbody>
      </v-table>
    </div>

    <div v-else class="card-body">
      <no-sheet-alert />
    </div>

    <!-- Modals -->
    <teleport to="body">
      <v-dialog id="search-records-modal" v-model="showSearchRecordsModal" width="400">
        <v-card title="Select columns">
          <v-card-text v-if="currentConnection">
            <p>Allow search on the specified columns</p>
            <v-switch v-for="column in currentConnection.columns" :key="column" :label="column" inset hide-details />
          </v-card-text>

          <v-card-actions>
            <button @click="showSearchRecordsModal = false">
              Cancel
            </button>
            <button>
              Validate
            </button>
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
                  <button-toggle color="warning" multiple>
                    <button value="creation">Create</button>
                    <button value="update">Update</button>
                  </button-toggle>
                </div>
              </div> -->
            </div>

            <!-- <v-switch v-for="column in blockDetails.record_creation_columns" :key="column" :label="column" inset hide-details /> -->
          </v-card-text>

          <v-card-actions>
            <button>Cancel</button>
            <button>Validate</button>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </teleport>

    <teleport to="body">
      <v-dialog id="column-update-modal" v-model="showColumnActionsModal" width="500">
        <v-card>
          <v-card-text>
            <v-text-field v-model="currentUpdatedColumn.name" label="Column name" variant="outlined" />
            <v-select v-model="currentUpdatedColumn.column_type" :items="columnTypeChoices" label="Column type" variant="outlined" />
            <v-select v-model="currentUpdatedColumn.column_sort" :items="columnSortingChoices" label="Sort" variant="outlined" clearable hide-details />
            <v-switch v-model="currentUpdatedColumn.allow_column_creation" label="Allow column creation" inset hide-details />
            <v-switch v-model="currentUpdatedColumn.allow_column_update" label="Allow column update" inset hide-details />
            <v-switch v-model="currentUpdatedColumn.allow_column_search" label="Allow column search" inset hide-details />
            <v-switch v-model="currentUpdatedColumn.column_visibility" label="Visibility" inset hide-details />
          </v-card-text>

          <v-card-actions>
            <button class="btn btn-light btn-rounded" @click="showColumnActionsModal = false">
              Cancel
            </button>
            <button class="btn btn-light btn-rounded" @click="handleUpdateColumn">
              Validate
            </button>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </teleport>
  </div>
</template>

<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { useBlocksComposable } from 'src/composables/blocks'
import { DefaultColumnTypes, DefaultSortingChoices } from 'src/data'
import { api } from 'src/plugins'
import { useDatasource } from 'src/stores/datasources'
import { useSlides } from 'src/stores/slides'
import { onBeforeMount, PropType, ref } from 'vue'

import type { BlockItem, ColumnTypes, DataSource, VisibleColumns } from 'src/types'

import NoSheetAlert from '../NoSheetAlert.vue'

interface ColumRequestData {
  name: string
  column_type: DefaultColumnTypes
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

const { columnTypeChoices, columnSortingChoices } = useBlocksComposable()
const slidesStore = useSlides()

const { currentSlide, blockRequestData, currentBlock } = storeToRefs(slidesStore)

const datasourceStore = useDatasource()
const { currentConnection } = storeToRefs(datasourceStore)

const columnsRequestData = ref<Record<string, ColumRequestData>>({})

const blockDatasource = ref<DataSource>()
const showCreateRecordModal = ref<boolean>(false)
const showSearchRecordsModal = ref<boolean>(false)
const showColumnActionsModal = ref<boolean>(false)
const currentUpdatedColumn = ref<ColumRequestData | null>(null)

/**
 * Updates the current column conffiguration
 * for the current block
 */
async function handleUpdateColumn() {
  try {
    if (currentSlide.value) {
      const path = `/api/v1/slides/${currentSlide.value.slide_id}/blocks/${currentBlock.block_id}/column/update`
      const response = await api.post(path, columnsRequestData.value[currentUpdatedColumn.value.name])

      currentBlock.visible_columns = response.data.visible_columns
      currentBlock.search_columns = response.data.search_columns
      currentBlock.record_update_columns = response.data.record_update_columns
      currentBlock.record_creation_columns = response.data.record_creation_columns
      showColumnActionsModal.value = false
    }
  } catch (e) {
    console.log(e)
  }
}

/**
 * Shows the modal to set specific actions
 * on a give column (search, visibility...)
 *
 * @param columnName The name of the column
 */
function handleShowColumnActionModal(column: VisibleColumns) {
  columnsRequestData.value[column.name] = {
    name: column.name,
    column_type: 'Text',
    column_sort: 'No sort',
    column_visibility: props.blockDetails.visible_columns.includes(column.name),
    allow_column_creation: props.blockDetails.record_creation_columns.includes(column.name),
    allow_column_update: props.blockDetails.record_update_columns.includes(column.name),
    allow_column_search: props.blockDetails.search_columns.includes(column.name)
  }

  currentUpdatedColumn.value = columnsRequestData.value[column.name]
  showColumnActionsModal.value = true
}

/**
 * Highlights the block when the user
 * has clicked on the card
 */
function handleBlockSelection() {
  slidesStore.setCurrentBlockRequestData()
  emit('block-selected', props.blockDetails)
}

onBeforeMount(() => {
  blockDatasource.value = props.blockDetails.block_data_source || currentSlide.value?.slide_data_source
})
</script>
