<template>
  <section id="database-tables">
    <nuxt-container>
      <div v-if="currentDatabase" class="mx-auto">
        <nuxt-card v-for="table in currentDatabase.tables" :key="table.id" class="mb-4">
          <template #header>
            <h2 class="text-lg font-medium flex items-center gap-2">
              <icon name="i-lucide-table" />
              {{ table.name }}
            </h2>
          </template>

          <div v-for="column in selectDocument(table)?.column_types || []" :key="column.name" class="py-2 px-5 border border-slate-100 flex items-center gap-2">
            <icon :name="getTypeIcon(column.columnType)" class="text-2xl" /> {{ column.name }}
          </div>
        </nuxt-card>
      </div>
      <div v-else>
        <nuxt-skeleton class="w-full h-4/6" />
      </div>
    </nuxt-container>
  </section>
</template>

<script setup lang="ts">
import { useColumnTypeOptions, useTableActualDocument } from '~/composables/use/documents'
import type { SimpleTable } from '~/types'

definePageMeta({
  title: 'Database: Tables',
  layout: 'details'
})

/**
 * Tables
 */

const databasesStore = useDatabasesStore()
const { currentDatabase } = storeToRefs(databasesStore)

/**
 * Select the current document object from a table
 * @param table The table to select the document from
 */
function selectDocument(table: SimpleTable) {
  return useTableActualDocument(table).value
}

/**
 * Other
 */

const { getTypeIcon } = useColumnTypeOptions()
</script>
