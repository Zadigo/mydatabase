<template>
  <div id="table" ref="tableEl" class="bg-white shadow-sm w-50 rounde-md rounded-md border-slate-100 z-40" :style="style" style="position: fixed">
    <div class="bg-slate-300 p-2 rounded-t-md font-bold flex items-center justify-between">
      <nuxt-button variant="ghost" color="neutral" icon="i-lucide-table" :disabled="true">
        {{ table.name }}
      </nuxt-button>

      <nuxt-button :to="`/databases/${dbStore.currentDatabase?.id}/editor?table=${table.id}`" size="sm" icon="i-lucide-link" variant="soft" />
    </div>

    <ul class="cursor-move overflow-y-scroll h-70">
      <li v-for="typeOption in tableDocument?.column_types || []" :key="typeOption.name" class="p-2 not-last:border-b border-slate-100 text-sm space-y-2 flex justify-between items-center">
        <div class="space-x-2">
          <span>{{ typeOption.name }}</span>
        </div>

        <div class="text-slate-500">
          <icon :name="getTypeIcon(typeOption.columnType)" class="text-md" />
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { useColumnTypeOptions, useTableActualDocument } from '~/composables/use/documents'
import type { Table } from '~/types'

const props = defineProps<{ table: Table }>()

/**
 * Dragging
 */

const containerEl = ref<HTMLElement | null>(null)
const tableEl = useTemplateRef('tableEl')

const { style } = useDraggable(tableEl, {
  initialValue: { x: 800, y: 200 },
  containerElement: containerEl,
  preventDefault: true
})

onMounted(() => {
  containerEl.value = document.querySelector('#tables-wrapper')
})

/**
 * Link
 */

const dbStore = useDatabasesStore()

/**
 * Columns
 */

const { getTypeIcon } = useColumnTypeOptions()
const tableDocument = useTableActualDocument(props.table)
</script>
