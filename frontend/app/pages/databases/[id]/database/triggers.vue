<template>
  <section id="database-triggers">
    Database triggers
  </section>
</template>

<script setup lang="ts">
definePageMeta({
  title: 'Database triggers',
  layout: 'details'
})

const dbStore = useDatabasesStore()
const { currentAside } = storeToRefs(dbStore)

currentAside.value = 'database-aside'

onUnmounted(() => {
  currentAside.value = null
})
</script>
