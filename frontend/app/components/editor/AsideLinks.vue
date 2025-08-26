<template>
  <div class="space-y-2">
    <!-- Select Table -->
    <nuxt-select-menu v-model="selectedTableName" :items="availableTables" value-key="name" label-key="name" class="w-full" placeholder="Select a table" />

    <!-- Select Table Data -->
    <nuxt-select-menu v-model="selectedTableDocumentName" :items="selectedTableDocumentNames" class="w-full" placeholder="Select a datasource" />

    <!-- Columns -->
    <editor-column-option-block :column-options="columnOptions" title="Column visibility">
      <template #default="{ column }">
        <span class="text-sm">{{ column.name }}</span>

        <div id="actions">
          <nuxt-button size="sm" variant="subtle" @click="() => toggleOption(column, 'visible')">
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
  </div>
</template>

<script setup lang="ts">
const dbStore = useDatabasesStore()
const { availableTables } = storeToRefs(dbStore)

const { selectedTableName, selectedTable, selectedTableDocumentName, selectedTableDocumentNames, tableData } = storeToRefs(useTableEditionStore())
const { columnOptions, toggleOption } = useTableColumns(tableData.value)
</script>
