<template>
  <div>
    <!-- Select Table -->
    <nuxt-select-menu v-model="selectedTable" :items="availableTableNames" class="w-full" />

    <!-- Columns -->
    <div v-if="columnOptions" class="mt-3 mb-5 rounded-lg">
      <h3 class="font-semibold mb-2">Columns</h3>
      <ul class=" bg-gray-200 rounded-lg">
        <li v-for="column in columnOptions" :key="column.name" class="px-4 py-2 flex justify-between not-last:border-b border-gray-100">
          <span class="text-sm">{{ column.name }}</span>

          <div>
            <nuxt-button size="sm" variant="subtle" @click="() => toggleOption(column, 'visible')">
              <icon v-if="column.visible" name="i-fa7-solid:eye" />
              <icon v-else name="i-fa7-solid:eye-slash" />
            </nuxt-button>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
const dbStore = useDatabasesStore()
const { availableTableNames } = storeToRefs(dbStore)

const { selectedTable } = storeToRefs(useTableEditionStore())
const { selectedTable: selectedTableObject } = useTable(selectedTable)
const { columnOptions, toggleOption } = useTableColumns(selectedTableObject.value?.documents)
</script>
