<template>
  <div id="table" ref="tableEl" class="bg-white shadow-sm w-50 rounde-md rounded-md border-slate-100 z-40" :style="style" style="position: fixed">
    <div class="bg-slate-300 p-2 rounded-t-md font-bold">
      <icon name="i-lucide-table" />
      {{ table.name }}
    </div>

    <ul class="cursor-move">
      <li v-for="i in 5" :key="i" class="p-2 not-last:border-b border-slate-100 text-sm space-y-2 flex justify-between items-center">
        <div class="space-x-2">
          <span>Column {{ i }}</span>
        </div>

        <div class="text-slate-500">
          <icon name="i-lucide-a-large-small text-md" />
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import type { Table } from '~/types'

defineProps<{ table: Table }>()

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
</script>
