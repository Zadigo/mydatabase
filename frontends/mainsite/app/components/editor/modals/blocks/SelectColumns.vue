<template>
  <form id="select-columns" @submit.prevent>
    <div v-for="name in names" :key="name">
      <h4 class="font-semibold p-5 rounded-lg bg-slate-100 dark:bg-slate-800 mb-5">{{ name }}</h4>
      <base-column-type-option v-for="(columnType, idx) in checkedoutResponses[name]?.columnTypes" :key="idx" :column-type="columnType" />
    </div>
  </form>
</template>

<script setup lang="ts">
const { checkedoutResponses, names } = useDocumentCheckoutStore()
</script>
