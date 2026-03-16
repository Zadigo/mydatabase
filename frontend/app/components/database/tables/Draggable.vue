<template>
  <div id="database-table" ref="tableEl" class="fixed bg-white dark:bg-slate-500 shadow-sm w-50 rounde-md rounded-md border-slate-100 z-40" :style="style">
    <div class="bg-slate-300 dark:bg-slate-600 p-2 rounded-t-md font-bold flex items-center justify-between">
      <nuxt-button variant="ghost" color="neutral" icon="i-lucide-table" :disabled="true">
        {{ table.name }}
      </nuxt-button>

      <nuxt-button :to="`/databases/${dbStore.currentDatabase?.id}/editor?table=${table.id}`" size="sm" icon="i-lucide-link" variant="soft" />
    </div>

    <ul class="cursor-move overflow-y-scroll h-70">
      <template v-if="isDefined(tableDocument)">
        <li v-for="name in tableDocument?.column_names || []" :key="name" :class="theme">
          <div class="space-x-2">
            <span>
              {{ name }}
            </span>
          </div>
  
          <div class="text-slate-500">
            <icon :name="getTypeIcon('String')" class="text-md" />
          </div>
        </li>
      </template>

      <template v-else>
        <li :class="theme">
          No active data source
        </li>
      </template>
    </ul>
  </div>
</template>

<script setup lang="ts">
import type { Table } from '~/types'

const { table, containerEl } = defineProps<{ table: Table, containerEl: HTMLElement | null }>()

/**
 * Dragging
 */

const tableEl = useTemplateRef('tableEl')

const { style } = useDraggable(tableEl, {
  initialValue: { x: 800, y: 200 },
  containerElement: containerEl
})

/**
 * Current Database
 */

const dbStore = useDatabasesStore()

/**
 * Current Table
 */

const tableEdition = useTableEditionStore()

/**
 * Columns
 */

const { getTypeIcon } = useColumnTypeOptions()
const tableDocument = useTableActualDocument(table)

/**
 * Utils
 */

const theme = `p-2 not-last:border-b border-slate-100 text-sm space-y-2 flex justify-between items-center`
</script>
