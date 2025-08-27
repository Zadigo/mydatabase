<template>
  <div class="space-y-2">
    <!-- Select Table -->
    <nuxt-select-menu v-model="selectedTableName" :items="availableTables" value-key="name" label-key="name" class="w-full" placeholder="Select a table" />

    <nuxt-button variant="soft" color="info" @click="() => { }">
      <icon name="i-lucide-plus" />
      Create table
    </nuxt-button>

    <!-- Select Table Data -->
    <nuxt-select-menu v-model="selectedTableDocumentName" :items="selectedTableDocumentNames" class="w-full" placeholder="Select a datasource" />

    <!-- Add Data -->
    <nuxt-button variant="soft" color="info" @click="() => { toggleShowAddDocumentModal() }">
      <icon name="i-lucide-file-plus-2" />
      Add document
    </nuxt-button>

    <!-- Columns -->
    <editor-column-option-block :column-options="columnOptions" title="Column visibility">
      <template #default="{ column }">
        <span :title="column.name" class="text-sm">{{ truncate(column.name, 15) }}</span>

        <div id="actions">
          <nuxt-button size="sm" variant="subtle" @click="() => tableColumnsStore.toggleOption(column, 'visible')">
            <icon v-if="column.visible" name="i-fa7-solid:eye" />
            <icon v-else name="i-fa7-solid:eye-slash" />
          </nuxt-button>
        </div>
      </template>
    </editor-column-option-block>

    <!-- Foreign Key -->
    <nuxt-input :disabled="true" icon="i-lucide-arrow-up-right" class="w-full" placeholder="Foreign table" />
    <nuxt-input :disabled="true" class="w-full" placeholder="Table key" />
    <nuxt-input :disabled="true" class="w-full" placeholder="Foreign key" />

    <!-- Options: Other -->
    <div v-if="selectedTable" class="mt-3 mb-5 rounded-lg">
      <div class="bg-gray-200 rounded-lg px-4 py-2 space-y-2">
        <nuxt-switch v-model="selectedTable.active" label="Active" />
        <nuxt-switch :disabled="true" label="Realtime" />
      </div>
    </div>
    <nuxt-skeleton v-else class="h-3 w-5" />

    <!-- Modals -->
    <editor-modals-add-document v-model="showAddDocumentModal" />
    <editor-modals-create-table v-model="showCreateTableModal" />
  </div>
</template>

<script setup lang="ts">
import { useCreateDocument } from '~/composables/use/documents'
import { useCreateTable } from '~/composables/use/tables'

const dbStore = useDatabasesStore()
const { availableTables } = storeToRefs(dbStore)

const { selectedTableName, selectedTable, selectedTableDocumentName, selectedTableDocumentNames, tableData } = storeToRefs(useTableEditionStore())
console.log('Editor.AsideLinks', tableData.value)

const tableColumnsStore = useTableColumnsStore()
const { columnOptions } = storeToRefs(tableColumnsStore)

/**
 * Fix titles 
 */

const { truncate } = useTruncateString()

/**
 * Create document
 */

const { showAddDocumentModal, toggleShowAddDocumentModal } = useCreateDocument()

/**
 * Create table
 */

const { showModal: showCreateTableModal } = useCreateTable()
</script>
