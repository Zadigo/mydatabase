<template>
  <div id="select-columns">
    {{ fileCheckoutResponse }}
    <lazy-base-column-type-option v-for="(columnType, idx) in fileCheckoutResponse?.columnTypes" :key="idx" :column-type="columnType" hydrate-on-visible />
  </div>
</template>

<script setup lang="ts">
const { fileCheckoutResponse } = useFileCheckoutStore()
</script>
