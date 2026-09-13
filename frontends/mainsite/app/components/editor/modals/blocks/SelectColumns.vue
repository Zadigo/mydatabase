<template>
  <form id="select-columns" @submit.prevent>
    <lazy-base-column-type-option v-for="(columnType, idx) in fileCheckoutResponse?.columnTypes" :key="idx" :column-type="columnType" hydrate-on-visible />
  </form>
</template>

<script setup lang="ts">
const { fileCheckoutResponse } = usePrefetchStore()
</script>
