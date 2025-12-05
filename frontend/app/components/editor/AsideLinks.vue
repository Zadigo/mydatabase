<template>
  <div class="space-y-2">
    <!-- Select Table -->
    <nuxt-select-menu v-model="selectedTableName" :items="availableTables" value-key="name" label-key="name" class="w-full" placeholder="Select a table" />

    <nuxt-button icon="i-lucide-plus" label="Create" size="sm" variant="soft" color="info" @click="() => { toggleCreateTable() }" />

    <dev-only>
      <p>
        hasDocuments {{ hasDocuments }} {{ selectedTableDocumentNames }}
      </p>
    </dev-only>
      
    <!-- Select Data -->
    <nuxt-select-menu v-model="selectedTableDocumentName" :items="selectedTableDocumentNames" class="w-full" placeholder="Select a datasource" />

    <!-- Data Actions -->
    <div class="space-x-2">
      <nuxt-button icon="i-lucide-file-plus-2" label="Add" size="sm" variant="soft" color="info" @click="() => { toggleShowAddDocumentModal() }" />
      <nuxt-button icon="i-lucide-pen" label="Update" size="sm" variant="soft" color="info" @click="() => { toggleShowEditDocumentModal()  }" />
    </div>

    <!-- Columns -->
    <editor-column-option-block :column-options="columnOptions" title="Column visibility">
      <template #default="{ column }">
        <nuxt-tooltip :text="column.name">
          <span class="text-sm">{{ truncate(column.name, 15) }}</span>
        </nuxt-tooltip>

        <div id="actions">
          <nuxt-button color="info" size="sm" variant="soft" @click="() => tableColumnsStore.toggleOption(column, 'visible')">
            <icon v-if="column.visible" name="i-fa7-solid:eye" />
            <icon v-else name="i-fa7-solid:eye-slash" />
          </nuxt-button>
        </div>
      </template>
    </editor-column-option-block>

    <!-- Options: Other -->
    <div v-if="selectedTable" class="mt-3 mb-5 rounded-lg">
      <div class="bg-gray-200 rounded-lg px-4 py-2 space-y-2">
        <nuxt-switch v-model="selectedTable.active" label="Active" />
        <nuxt-switch :disabled="true" label="Realtime" />
      </div>
    </div>

    <!-- Delete -->
    <nuxt-button :disabled="!selectedTable" variant="subtle" color="error" label="Delete table" block />
  </div>
</template>

<script setup lang="ts">
import { useCreateDocument, useEditDocument } from '~/composables/use/documents'
import { useCreateTable } from '~/composables/use/tables'

const dbStore = useDatabasesStore()
const { availableTables } = storeToRefs(dbStore)

const { hasDocuments, selectedTableName, selectedTable, selectedTableDocumentName, selectedTableDocumentNames, tableData } = storeToRefs(useTableEditionStore())

console.log('Editor.AsideLinks', tableData.value)

/**
 * Url query parameters
 */

const queryParams = useUrlSearchParams() as { table: string }
watch(selectedTableDocumentName, (value) => {
  if (value) {
    queryParams.table = useToString(selectedTable.value?.id || '').value
  }
})


/**
 * Columns
 */

const tableColumnsStore = useTableColumnsStore()
const { columnOptions } = storeToRefs(tableColumnsStore)

/**
 * Fix column names 
 */

const { truncate } = useTruncateString()

/**
 * Create document
 */

const { toggleShowAddDocumentModal } = useCreateDocument()

/**
 * Create table
 */

const { toggleCreateTable } = useCreateTable()

/**
 * Update document
 */

const { toggleShowEditDocumentModal } = useEditDocument()
</script>
