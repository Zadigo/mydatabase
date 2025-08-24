<template>
  <section id="data-table">
    {{ items }}
    <nuxt-table v-if="items" :items="items" />
    <div v-else>
      <nuxt-skeleton class="h-10 w-full" />
      <nuxt-skeleton class="h-10 w-6/12" />
      <nuxt-skeleton class="h-10 w-4/12" />
    </div>
  </section>
</template>

<script setup lang="ts">
import type { DocumentData } from '~/types'
import type { ComputedRef } from 'vue'

const items = inject<ComputedRef<DocumentData[]>>('tableData')
console.log(items)
</script>
