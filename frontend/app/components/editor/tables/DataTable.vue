<template>
  <section id="data-table">
    <nuxt-table v-if="items" v-model:column-visibility="columnVisibility" :data="items" :columns="tableColumns" :sticky="true" />
    <div v-else>
      <nuxt-skeleton class="h-10 w-full" />
      <nuxt-skeleton class="h-10 w-6/12" />
      <nuxt-skeleton class="h-10 w-4/12" />
    </div>
  </section>
</template>

<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'
// import { h } from 'vue'
import type { DocumentData } from '~/types'

const items = inject<ComputedRef<DocumentData[]>>('tableData')

const tableColumnsStore = useTableColumnsStore()
const { columnNames, columnOptions } = storeToRefs(tableColumnsStore)

/**
 * Columns
 */

const tableColumns = computed<TableColumn<DocumentData>[]>(() => {
  return columnNames.value.map(column => ({
    accessorKey: column,
    header: column,
    enableHiding: true
  }))
})

/**
 * Visibility
 */

const columnVisibility = computed(() => {
  return columnOptions.value.reduce((acc, option) => {
    acc[option.name] = option.visible
    return acc
  }, {} as Record<string, boolean>)
})
</script>
