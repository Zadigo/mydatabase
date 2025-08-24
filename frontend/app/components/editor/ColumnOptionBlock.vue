<template>
  <div class="mt-3 mb-5 rounded-lg">
    <h3 class="font-semibold mb-2">
      {{ title }}
    </h3>
    
    <ul class="bg-gray-200 rounded-lg">
      <li v-for="column in columnOptions" :key="column.name" class="px-4 py-2 flex justify-between not-last:border-b border-gray-100">
        <slot :column="column" />
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import type { ColumnOptions } from '~/composables/use/tables'

defineProps<{ title: string, columnOptions: ColumnOptions[] }>()
</script>
