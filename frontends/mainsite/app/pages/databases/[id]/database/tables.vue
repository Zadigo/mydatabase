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
          
          <div v-for="column in selectDocument(table)?.column_options || []" :key="column.name" class="py-2 px-5 border border-slate-100 dark:border-slate-700 first:rounded-tr-lg first:rounded-tl-lg last:rounded-bl-lg last:rounded-br-lg flex items-center gap-2">
            <icon :name="getTypeIcon(column.columnType)" class="text-2xl" />
            <span>{{ column.name }}</span>
          </div>
        </nuxt-card>
      </div>
      <div v-else>
        NO DATASOURCE SELECTED
        <nuxt-skeleton class="w-full h-4/6" />
      </div>
    </nuxt-container>
  </section>
</template>

<script setup lang="ts">
import type { SimpleTable } from '#shared/types'

definePageMeta({
  label: 'Database: Tables',
  layout: {
    name: 'details',
    props: {
      asideName: 'database'
    }
  }
})

/**
 * Tables
 */

const { currentDatabase } = _useDatabases() 

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
