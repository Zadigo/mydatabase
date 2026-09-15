<template>
  <form id="select-columns" @submit.prevent>
    <div v-for="name in names" :key="name" class="p-3 bg-slate-200 dark:bg-slate-950 rounded-lg">
      <h4 class="font-semibold p-5 rounded-lg bg-slate-100 dark:bg-slate-800 mb-5">{{ name }}</h4>
      <base-column-type-option v-for="(columnOption, idx) in getColumnOptions(name)" :key="idx" :index="idx" :column-option="columnOption" />
    </div>
  </form>
</template>

<script setup lang="ts">
const { fileCheckoutResponse, names } = useDocumentCheckoutStore()

const getColumnOptions = (name: string) => {
  return fileCheckoutResponse.value[name]?.columnTypes || []
}
</script>
