<template>
  <section id="data-table">
    <nuxt-table v-if="items" :data="items" sticky />
    <div v-else>
      <nuxt-skeleton class="h-10 w-full" />
      <nuxt-skeleton class="h-10 w-6/12" />
      <nuxt-skeleton class="h-10 w-4/12" />
    </div>
  </section>
</template>

<script setup lang="ts">
// import type { TableColumn } from '@nuxt/ui'
// import { h } from 'vue'
import type { DocumentData } from '~/types'
import type { ComputedRef } from 'vue'

const items = inject<ComputedRef<DocumentData[]>>('tableData')
console.log('DataTable', items)

// const tableColumns = ref<TableColumn<DocumentData>[]>([])
</script>
